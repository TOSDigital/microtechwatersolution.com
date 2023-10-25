from django import forms
from mainapp.models import ServiceDeskUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class ServiceDeskUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
    service_desk_name = forms.CharField()
    service_desk_email = forms.EmailField()
    service_desk_phone = forms.CharField()