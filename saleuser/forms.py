from django import forms
from mainapp.models import SalesLogin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SaleUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
    saleuser_name = forms.CharField()
    saleuser_email = forms.EmailField()
    saleuser_phone = forms.CharField()