from django import forms

class AttandenceForm(forms.Form):
    document = forms.FileField(
        label='Choose a file'
    )