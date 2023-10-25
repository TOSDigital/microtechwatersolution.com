from django.urls import path, include
from .views import SaleUserListView, SaleUserCreateView, SaleUserDetailView, SaleUserUpdateView, SaleUserDeleteView


app_name = 'saleuser'


urlpatterns = [
    path('saleusers/', SaleUserListView.as_view(), name='saleuserslist'),
    
    path('saleuserscreate/', SaleUserCreateView.as_view(), name='saleuserscreate'),
    path('saleusersdetail/<int:pk>', SaleUserDetailView.as_view(), name='saleusersdetail'),
    path('saleusersupdate/<int:pk>', SaleUserUpdateView.as_view(), name='saleusersupdate'),
    path('saleusersdelete/<int:pk>', SaleUserDeleteView.as_view(), name='saleusersdelete'),
]