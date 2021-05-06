from django.shortcuts import render, redirect
from .models import User, Attandence, Department, AttandenceTable
from django.contrib import messages
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from .forms import AttandenceForm
import bcrypt 

def index(request):
    if request.method == "GET":
        return render(request,"index.html")

def register(request):
    if request.method == "GET":
        context = {
            'all_departments' : Department.objects.all(),
            'today': date.today()
        }
        return render(request,"register.html", context)
    
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        print(pw_hash)
        the_position = False
        if request.POST['position'] == "true":
            the_position = True
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            birthday = request.POST['birthday'],
            position = the_position,
            user_name = request.POST['user_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        this_department = Department.objects.get(id=request.POST['department'])
        this_user = User.objects.get(id=new_user.id)
        this_department.users.add(this_user)
        request.session['uid'] = new_user.id
        if new_user.position == True:
            return redirect('/admin')
        else:
            return redirect("/employee")

def login(request):
    if request.method == "GET":
        return render(request,"login.html")

    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
    
        user_list = User.objects.filter(user_name=request.POST['user_name'])
        if user_list:
            logged_user = user_list[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['uid'] = logged_user.id
                if logged_user.position == True:
                    return redirect('/admin')
                else:
                    return redirect("/employee")

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def admin_page(request):
    if request.method == "GET":
        if 'uid' in request.session:
            this_user= User.objects.get(id=request.session['uid'])
        if this_user.position==True:
            context = {
                'all_users' : User.objects.all(),
                'all_departments' : Department.objects.all()
            }
            return render(request,"admin.html",context)
    return redirect('/')

def employee_page(request):
    if request.method == "GET":
        if 'uid' in request.session:
            this_user= User.objects.get(id=request.session['uid'])
        if this_user.position==False:
            context = {
                'this_user':this_user,
                'all_users': User.objects.all()
            }
            return render(request,"employee.html", context)
    return redirect('/')

def add_emp(request):
    if request.method == "GET":
        context = {
            'all_departments' : Department.objects.all(),
            'today': date.today()
        }
        return render(request,"add_emp.html", context)

    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_emp')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        print(pw_hash)
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            birthday = request.POST['birthday'],
            user_name = request.POST['user_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        this_department = Department.objects.get(id=request.POST['department'])
        this_user = User.objects.get(id=new_user.id)
        this_department.users.add(this_user)
        return redirect('/admin')

def edit_emp(request, emp_id):
    if request.method == "GET":
        context = {
            'emp' : User.objects.get(id=emp_id),
            'all_departments' : Department.objects.all(),
        }
        return render(request,"edit_emp.html", context)

    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit_emp/{emp_id}')

        emp = User.objects.get(id=emp_id)
        emp.first_name = request.POST['first_name']
        emp.last_name = request.POST['last_name']
        emp.email = request.POST['email']
        this_department = Department.objects.get(id=request.POST['department'])
        this_department.users.add(emp)
        emp.save()
        return redirect('/admin')

def remove_emp(request, emp_id):
    emp = User.objects.get(id=emp_id)
    emp.delete()
    return redirect('/admin')

def calculate_salary(request, emp_id):
    if request.method == "GET":
        emp = User.objects.get(id=emp_id)
        #total_salary = emp.salary_per_day * 30
        context = {
            'emp' : emp,
        }
        return render(request,"salary_cal.html", context)

    if request.method == "POST":
        emp = User.objects.get(id=emp_id)
        salary_per_day = request.POST['salary_per_day']
        days = request.POST['days']
        emp.total_salary = float(salary_per_day) * int(days)
        emp.save()
        return redirect(f'/calculate_salary/{emp_id}')

def upload_user_attandence(request):
    if request.method == "POST":
        form = AttandenceForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Attandence(description = request.POST['desc'], document = request.FILES['document'])
            newdoc.save()
            return redirect('/upload')
        
    else:
        form = AttandenceForm()
        users_attandences = Attandence.objects.all()
        context = {
            'form' : form,
            'attandences' : users_attandences
        }
        return render(request, "user_attandance.html", context)

def edit_info(request):
    if request.method == "GET":
        context = {
            'emp' : User.objects.get(id=request.session['uid']),
            'all_departments' : Department.objects.all(),
            'today':date.today()
        }
        return render(request,"edit_info.html", context)

    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_info')

        emp = User.objects.get(id=request.session['uid'])
        emp.first_name = request.POST['first_name']
        emp.last_name = request.POST['last_name']
        emp.email = request.POST['email']
        emp.birthday = request.POST['birthday']
        emp.save()
        return redirect('/employee')

def contact(request):
    if request.method == "GET":
        context = {
            'emp': User.objects.all()
        }
        return render(request, "contact.html", context)

    if request.method == "POST":
        message_name = request.POST['message_name']
        message = request.POST['message']

        for user in User.objects.all():
            send_mail(
                message_name,
                message,
                'spoiled.coders@gmail.com',
                [user.email]
            )
        return redirect('/admin')

def attandence(request):
        context = {
            'emp' : User.objects.all(),
            'date':date.today()
        }
        return render(request, "attandance.html", context)

def attended(request,emp_id):
    emp = User.objects.get(id=emp_id)
    AttandenceTable.objects.create(
        employee=emp,
        date= date.today(),
        attendence=True
    )
    return redirect('/attandence')

def absent(request,emp_id):
    emp = User.objects.get(id=emp_id)
    AttandenceTable.objects.create(
        employee=emp,
        date=date.today(),
        attendence=False
    )
    return redirect('/attandence')