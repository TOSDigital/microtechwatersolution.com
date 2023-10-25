from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from mainapp.models import TechnicianLogin
from .forms import TechnicianModelForm
from django.core.mail import send_mail
from saleuser.mixins import AdminAndLoginRequiredMixin

# Create your views here.


class TechnicianListView(LoginRequiredMixin, ListView):
    template_name = "technicianlist.html"
    
      # Set the model for the ListView

    def get_queryset(self):
        admin = self.request.user.userprofile
        service_desk = self.request.user.userprofile
        return TechnicianLogin.objects.filter(admin=admin, service_desk=service_desk)


class TechnicianCreateView(LoginRequiredMixin, CreateView):
    template_name = 'techniciancreate.html'
    form_class = TechnicianModelForm

    def get_success_url(self):
        return reverse("technician:Technicianlist")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_sales_login = False
        user.is_admin = False
        user.is_service_desk = False
        user.is_technician = True
        user.save()

        technician_name= form.cleaned_data['technician_name']
        technician_email = form.cleaned_data['technician_email']
        technician_phone = form.cleaned_data['technician_phone']

        service_desk_user = TechnicianLogin.objects.create(
            user=user,
            admin=self.request.user.userprofile,
            service_desk=self.request.user.userprofile,
            technician_name=technician_name,
            technician_email=technician_email,
            technician_phone=technician_phone
        )
        # Send an email
        send_mail(
            subject="You are invited to be a Service Department User",
            message="You were added as a Service Department User On Microtech Water Solutions. Please Login to the website to start working",
            from_email="theonesolutionmysore@gmail.com",
            recipient_list=[user.email]
        )

        return super(TechnicianCreateView, self).form_valid(form)


class TechnicianDetailView(LoginRequiredMixin, DetailView):
    template_name = "techniciandetail.html"
    context_object_name = "technicianlogin"

    def get_queryset(self):
        return TechnicianLogin.objects.all()

class TechnicianUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'technicianupdate.html'
    model = TechnicianLogin
    fields = (
        'technician_name',
        'technician_phone',
        'technician_email'
    )
    
    def get_success_url(self):
        return reverse("technician:Technicianlist")

    def get_queryset(self):
        return TechnicianLogin.objects.all()

class TechnicianDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'techniciandelete.html'
    context_object_name = 'techniciandelete'
    
    def get_success_url(self):
        return reverse("technician:Technicianlist")

    def get_queryset(self):
        return TechnicianLogin.objects.all()



