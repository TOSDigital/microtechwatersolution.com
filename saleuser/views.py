from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from mainapp.models import SalesLogin
from .forms import SaleUserModelForm
from django.core.mail import send_mail
from saleuser.mixins import AdminAndLoginRequiredMixin

# Create your views here.


class SaleUserListView(AdminAndLoginRequiredMixin, ListView):
    template_name = "saleuserlist.html"
    
      # Set the model for the ListView

    def get_queryset(self):
        admin = self.request.user.userprofile
        return SalesLogin.objects.filter(admin=admin)


class SaleUserCreateView(AdminAndLoginRequiredMixin, CreateView):
    template_name = 'saleusercreate.html'
    form_class = SaleUserModelForm

    def get_success_url(self):
        return reverse("saleuser:saleuserslist")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_sales_login = True
        user.is_admin = False
        user.is_service_desk = False
        user.is_technician = False
        user.save()

        saleuser_name = form.cleaned_data['saleuser_name']
        saleuser_email = form.cleaned_data['saleuser_email']
        saleuser_phone = form.cleaned_data['saleuser_phone']

        # Create a SalesLogin instance or any relevant model
        sales_login = SalesLogin.objects.create(
            user=user,
            admin=self.request.user.userprofile,
            saleuser_name=saleuser_name,
            saleuser_email=saleuser_email,
            saleuser_phone=saleuser_phone
        )
        # Send an email
        send_mail(
            subject="You are invited to be a Sale Department User",
            message="You were added as a Sale Department User On Microtech Water Solutions. Please Login to the website to start working",
            from_email="theonesolutionmysore@gmail.com",
            recipient_list=[user.email]
        )

        return super(SaleUserCreateView, self).form_valid(form)
class SaleUserDetailView(AdminAndLoginRequiredMixin, DetailView):
    template_name = "saleuserdetail.html"
    context_object_name = "saleslogin"

    def get_queryset(self):
        return SalesLogin.objects.all()

class SaleUserUpdateView(AdminAndLoginRequiredMixin, UpdateView):
    template_name = 'saleuserupdate.html'
    form_class = SaleUserModelForm
    
    def get_success_url(self):
        return reverse("saleuser:saleuserslist")

    def get_queryset(self):
        return SalesLogin.objects.all()

class SaleUserDeleteView(AdminAndLoginRequiredMixin, DeleteView):
    template_name = 'saleuserdelete.html'
    context_object_name = 'saleuserdelete'
    
    def get_success_url(self):
        return reverse("saleuser:saleuserslist")

    def get_queryset(self):
        return SalesLogin.objects.all()



