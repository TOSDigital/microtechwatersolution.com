from django import forms
from mainapp.models import TechnicianLogin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class TechnicianModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
    technician_name = forms.CharField()
    technician_email = forms.EmailField()
    technician_phone = forms.CharField()