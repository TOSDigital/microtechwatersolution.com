from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Customer, Products
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomerForm, CreateCustomUser, DateRangeForm, ProductForm, ServiceJobCreationForm
from django.db.models import Q
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_POST
from excel_response import ExcelResponse
import io
import pandas as pd
from datetime import datetime
from saleuser.mixins import AdminAndLoginRequiredMixin
from django.http import JsonResponse




class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CreateCustomUser

    def get_success_url(self):
        return reverse("login")

# customer List View

class CustomerListView(LoginRequiredMixin, ListView):
    template_name = "customerlist.html"
    queryset = Customer.objects.all().order_by('-id')
    context_object_name = "customers"

# customer database download feature

class ExcelDownloadView(LoginRequiredMixin, FormView):
    form_class = DateRangeForm
    template_name = "customerlist.html"

    def form_valid(self, form):
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']

        # Filter the customers based on the date range
        customers = Customer.objects.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date
        ).order_by('-id')

        # Create a Pandas DataFrame with the filtered data
        data = {
            "Customer Name": [customer.customer_name for customer in customers],
            "Customer Email": [customer.customer_email for customer in customers],
            "Customer Phone": [customer.customer_phone for customer in customers],
            "Customer Location": [customer.customer_location for customer in customers],
        }
        df = pd.DataFrame(data)

        # Create an Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Customer Data')

        output.seek(0)

        # Prepare the response with the Excel file
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=customer_data_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

        return response

        return HttpResponseRedirect(reverse('customerlist'))

# customer create 

class CustomerCreateView(LoginRequiredMixin, CreateView):
    template_name = "customercreate.html"
    form_class = CustomerForm

    def get_success_url(self):
        return reverse("customerlist")

# customer update

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customerupdate.html"
    model = Customer
    fields = (
        'customer_name',
        'customer_email',
        'customer_phone',
        'customer_location',

    )

    def get_success_url(self):
        return reverse("customerlist")

# customer delete

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "customerdelete.html"
    model = Customer
    context_object_name = "customer"

    def get_success_url(self):
        return reverse("customerlist")

# Search Feature

class SearchResultsView(LoginRequiredMixin, View):
    template_name = "searchcustomer.html"

    def post(self, request, *args, **kwargs):
        query = request.POST.get('q')
        if query:
            results = Customer.objects.filter(
                Q(customer_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(customer_phone__icontains=query) |
                Q(customer_email__icontains=query) |
                Q(customer_location__icontains=query) 

            ).order_by('-id')
        else:
            results = None

        return render(request, self.template_name, {'search_results': results})

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customerdetail.html"
    context_object_name = "customerdetail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.object.pk
        context['products'] = Products.objects.filter(Customer_id=customer_id)  # Retrieve the associated products
        return context
    

# product views

class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = "addproduct.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse("customerlist")

class ProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = "productlist.html"  # Create a new template for the product list
    context_object_name = "products"

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Products.objects.filter(Customer_id=customer_id)

class AllProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = "allproducts.html"  # Create a new template for displaying all products
    context_object_name = "products"

    def get_queryset(self):
        return Products.objects.all()  # Retrieve all products

class ServiceCreateView(LoginRequiredMixin, CreateView):
    template_name = "servicejobcreate.html"
    form_class = ServiceJobCreationForm

    def get_success_url(self):
        return reverse("customerlist")

