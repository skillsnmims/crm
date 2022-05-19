from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

from accounts import views

app_name = "accounts"

urlpatterns = [
    url(r"^login/$", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    url(r"^password/change/$", views.change_password, name="change_password"),
    url(r"^logout/$", logout_then_login, name="logout"),


]
