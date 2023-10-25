from django.contrib import admin
from django.urls import path
from . import views 
from .views import Dashboard, CustomerListView, CustomerCreateView, ExcelDownloadView, CustomerUpdateView, CustomerDeleteView, SearchResultsView, CustomerDetailView
from .views import ProductCreateView, ProductListView, AllProductListView
from .views import ServiceCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', Dashboard.as_view(), name='dashboard'),
   path('customerlist/', CustomerListView.as_view(), name='customerlist'),
   path('createcustomer/', CustomerCreateView.as_view(), name='customercreate'),
   path('<int:pk>/customerdetail/', CustomerDetailView.as_view(), name='customerdetails'),
   path('<int:pk>/updatecustomerdetails/', CustomerUpdateView.as_view(), name='customerupdate'),
   path('<int:pk>/deletecustomer/', CustomerDeleteView.as_view(), name='customerdelete'),
   path('search_results/', SearchResultsView.as_view(), name='search_results'),
   path('customer/download-excel/', ExcelDownloadView.as_view(), name='download_excel'),
   path('addproduct', ProductCreateView.as_view(), name='addproduct'),
   path('products/<int:pk>/', ProductListView.as_view(), name='productlist'),
   path('products/all/', AllProductListView.as_view(), name='allproducts'),
   path('createservicejob/', ServiceCreateView.as_view(), name='servicejobcreate'),
   # path('get_products/', views.get_products, name='get_products'),
   



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)