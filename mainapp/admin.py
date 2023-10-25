from django.contrib import admin
from .models import User, UserProfile, SalesLogin, ServiceDeskUser, TechnicianLogin, Customer, Products, ServiceDeskUser, TechnicianLogin, ServiceJob


# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(SalesLogin)
admin.site.register(ServiceDeskUser)
admin.site.register(TechnicianLogin)
admin.site.register(ServiceJob)