from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('admin', views.admin_page),
    path('employee', views.employee_page),
    path('add_emp', views.add_emp),
    path('edit_emp/<int:emp_id>', views.edit_emp),
    path('remove_emp/<int:emp_id>', views.remove_emp),
    path('calculate_salary/<int:emp_id>', views.calculate_salary),
    path('upload', views.upload_user_attandence),
    path('edit_info',views.edit_info),
    path('send_email', views.contact),
    path('attandence',views.attandence),
    path('attandence/<int:emp_id>/attended', views.attended),
    path('attandence/<int:emp_id>/absent', views.absent),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)