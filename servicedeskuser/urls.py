from django.urls import path, include
from .views import ServiceUserListView, ServiceUserCreateView, ServiceUserDetailView, ServiceUserUpdateView, ServiceUserDeleteView

app_name = 'servicedeskuser'


urlpatterns = [
    path('serviceusers/', ServiceUserListView.as_view(), name='serviceuserslist'),
    path('serviceuserscreate/', ServiceUserCreateView.as_view(), name='serviceuserscreate'),
    path('serviceusersdetail/<int:pk>', ServiceUserDetailView.as_view(), name='serviceusersdetail'),
    path('serviceusersupdate/<int:pk>', ServiceUserUpdateView.as_view(), name='serviceusersupdate'),
    path('serviceusersdelete/<int:pk>', ServiceUserDeleteView.as_view(), name='serviceusersdelete'),
]