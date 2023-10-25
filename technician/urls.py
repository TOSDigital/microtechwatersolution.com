from django.urls import path, include
from .views import TechnicianListView, TechnicianCreateView, TechnicianDetailView, TechnicianUpdateView, TechnicianDeleteView

app_name = 'technician'


urlpatterns = [
    path('technicians/', TechnicianListView.as_view(), name='Technicianlist'),
    path('technicianscreate/', TechnicianCreateView.as_view(), name='Techniciancreate'),
    path('stechniciansdetail/<int:pk>', TechnicianDetailView.as_view(), name='Techniciandetail'),
    path('techniciansupdate/<int:pk>', TechnicianUpdateView.as_view(), name='Technicianupdate'),
    path('techniciansdelete/<int:pk>', TechnicianDeleteView.as_view(), name='Techniciandelete'),
]