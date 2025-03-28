from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path(
        "management-dashboard/", views.management_dashboard, name="management_dashboard"
    ),
]
