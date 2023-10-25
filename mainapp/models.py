from django.db import models
import datetime
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def get_current_date():
    return timezone.now()

class User(AbstractUser): 
    is_admin = models.BooleanField(default=False)
    is_sales_login = models.BooleanField(default=False)
    is_service_desk = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    customer_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    company_name = models.CharField(max_length=100, default='Company')
    customer_email = models.EmailField() 
    customer_phone = models.CharField(max_length=10)
    customer_location = models.CharField(max_length=1000, null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=get_current_date)

    def __str__(self):
        return self.customer_name

class Products(models.Model):
    Product_name = models.CharField(max_length=200)
    Purchase_date = models.DateField()
    warranty = models.DateField()
    Warranty_end_date = models.DateField()
    Customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='Customer')

    def __str__(self):
        return f"{self.Product_name} - {self.Customer}"

    
    # def save(self, *args, **kwargs):
    #     # Populate the warranty field with the Purchase_date value
    #     self.warranty = self.Purchase_date
    #     super(Products, self).save(*args, **kwargs)

class SalesLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    saleuser_name = models.CharField(max_length=100)
    saleuser_email = models.EmailField()
    saleuser_phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class ServiceDeskUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service_desk_name = models.CharField(max_length=100)
    service_desk_email = models.EmailField()
    service_desk_phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class TechnicianLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_desk = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='service_desk_technicians')
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='admin_technicians')
    technician_name = models.CharField(max_length=100)
    technician_email = models.EmailField()
    technician_phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class ServiceJob(models.Model):
    SERVICE_DESK_CHOICES =(
        ('Created', 'Accepted'),
        ('Closed', 'Closed'),
    )

    TECHNICIAN_CHOICES =(
        ('Accepted', 'Accepted'),
        ('In-progress', 'In-progress'),
        ('Closed', 'Closed'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=1000)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=10)
    service_status = models.CharField(max_length=20, choices=SERVICE_DESK_CHOICES)
    Technician_service_status = models.CharField(max_length=20, choices=TECHNICIAN_CHOICES)



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)