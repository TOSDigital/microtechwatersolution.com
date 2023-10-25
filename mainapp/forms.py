from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'customer_name',
            'company_name',
            'customer_email',
            'customer_phone',
            'customer_location',

        )

class DateRangeForm(forms.Form):
    from_date = forms.DateField(
        label='From Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_date = forms.DateField(
        label='To Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class CreateCustomUser(UserCreationForm):
    class Meta:
        model = User
        fields = {"username",}
        field_classes = {'username': UsernameField}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'Product_name', 
            'Purchase_date', 
            'warranty',
            'Warranty_end_date',
            'Customer'
        
        )
        widgets = {
            'Purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty': forms.DateInput(attrs={'type': 'date'}),
            'Warranty_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceJobCreationForm(forms.ModelForm):
    class Meta:
        model = ServiceJob  # Set the model for the form
        fields = ['customer', 'product', 'customer_name', 'customer_email', 'customer_phone', 'service_status', 'Technician_service_status']  # Ensure field names are in lowercase

    

         