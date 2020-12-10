from django.urls import path, include
from . import views

from tasks import urls

#Ver como colocar las views de task aca. Mismo, reescribir la urls.py de la app principal. La app tasks y sus views, funcionan desde aca

urlpatterns = [
    path("", views.user_error_not_found, name="error-not-found"),
    path("account/login", views.login_render, name="login"),
    path("account/login/auth", views.login_user, name="login-auth"),
    path("account/logout", views.logout_user, name="logout"),
    path("account/register", views.register_render, name="register"),
    path("account/register/new", views.register_user, name="register-new"),
    path("dashboard", views.dashboard_user, name="dashboard"),
    path("dashboard/task/", include("tasks.urls"))
]
