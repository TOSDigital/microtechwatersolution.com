from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from mainapp.models import ServiceDeskUser
from .forms import ServiceDeskUserModelForm
from django.core.mail import send_mail
from saleuser.mixins import AdminAndLoginRequiredMixin

# Create your views here.


class ServiceUserListView(AdminAndLoginRequiredMixin, ListView):
    template_name = "serviceuserlist.html"
    
      # Set the model for the ListView

    def get_queryset(self):
        admin = self.request.user.userprofile
        return ServiceDeskUser.objects.filter(admin=admin)


class ServiceUserCreateView(AdminAndLoginRequiredMixin, CreateView):
    template_name = 'serviceusercreate.html'
    form_class = ServiceDeskUserModelForm

    def get_success_url(self):
        return reverse("servicedeskuser:serviceuserslist")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_sales_login = False
        user.is_admin = False
        user.is_service_desk = True
        user.is_technician = False
        user.save()

        service_desk_name= form.cleaned_data['service_desk_name']
        service_desk_email = form.cleaned_data['service_desk_email']
        service_desk_phone = form.cleaned_data['service_desk_phone']

        service_desk_user = ServiceDeskUser.objects.create(
            user=user,
            admin=self.request.user.userprofile,
            service_desk_name=service_desk_name,
            service_desk_email=service_desk_email,
            service_desk_phone=service_desk_phone
        )
        # Send an email
        send_mail(
            subject="You are invited to be a Service Department User",
            message="You were added as a Service Department User On Microtech Water Solutions. Please Login to the website to start working",
            from_email="theonesolutionmysore@gmail.com",
            recipient_list=[user.email]
        )

        return super(ServiceUserCreateView, self).form_valid(form)


class ServiceUserDetailView(AdminAndLoginRequiredMixin, DetailView):
    template_name = "serviceuserdetail.html"
    context_object_name = "servicelogin"

    def get_queryset(self):
        return ServiceDeskUser.objects.all()

class ServiceUserUpdateView(AdminAndLoginRequiredMixin, UpdateView):
    template_name = 'serviceuserupdate.html'
    model = ServiceDeskUser
    fields = (
        'service_desk_name',
        'service_desk_phone',
        'service_desk_email'
    )
    
    def get_success_url(self):
        return reverse("servicedeskuser:serviceuserslist")

    def get_queryset(self):
        return ServiceDeskUser.objects.all()

class ServiceUserDeleteView(AdminAndLoginRequiredMixin, DeleteView):
    template_name = 'serviceuserdelete.html'
    context_object_name = 'serviceuserdelete'
    
    def get_success_url(self):
        return reverse("servicedeskuser:serviceuserslist")

    def get_queryset(self):
        return ServiceDeskUser.objects.all()



