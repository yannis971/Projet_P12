"""
Module urls.py
"""
import django.contrib.auth.views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from crm_api import views

app_name = "crm_api"

router = DefaultRouter()
router.register(r"salescontacts",
                views.SalesContactViewSet,
                basename="salescontacts")
router.register(r"supportcontacts",
                views.SupportContactViewSet,
                basename="supportcontacts")
router.register(r"staffcontacts",
                views.StaffContactViewSet,
                basename="staffcontacts")
router.register(r"clients",
                views.ClientViewSet,
                basename="clients")
router.register(r"contracts",
                views.ContractViewSet,
                basename="contracts")
router.register(r"events",
                views.EventViewSet,
                basename="events")

urlpatterns = [
    path("api/login/", views.LoginView.as_view(), name="api-login"),
    path("api/logout/", views.LogoutView.as_view(), name="api-logout"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="crm_admin/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="crm_api/logged_out.html"),
        name="logout",
    ),
    path("init_database/",
         views.InitDataBaseView.as_view(),
         name="init_database"),
    path("", include(router.urls)),
]
