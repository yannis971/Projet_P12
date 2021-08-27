
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from crm_api import views

app_name = 'crm_api'

router = DefaultRouter()
router.register(r'salescontacts', views.SalesContactViewSet, basename='salescontacts')
# generates:
# /salescontacts/
# /salescontacts/{pk}/

urlpatterns = [
    path('',  views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
