
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from crm_api import views

app_name = 'crm_api'

router = DefaultRouter()
router.register(r'salescontacts', views.SalesContactViewSet, basename='salescontacts')
router.register(r'supportcontacts', views.SupportContactViewSet, basename='supportcontacts')
router.register(r'staffcontacts', views.StaffContactViewSet, basename='staffcontacts')
router.register(r'clients', views.ClientViewSet, basename='clients')
router.register(r'contracts', views.ContractViewSet, basename='contracts')
router.register(r'events', views.EventViewSet, basename='events')

urlpatterns = [
    path('',  views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path('', include(router.urls)),
]
