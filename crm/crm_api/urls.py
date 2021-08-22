
from django.urls import path
from .views import home
app_name = 'crm_api'
urlpatterns = [
    path('',  home, name='home'),
]
