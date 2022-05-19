from django.conf.urls import url
from . import views

app_name = "portal"

urlpatterns = [
    url(r"^$", views.DashboardView.as_view(), name="dashboard"),
    url(r"^call/$", views.calling_page, name="calling_page"),
    # url(r"^test/$", views.test, name="test"),
    # url(r"^call/response/$", views.save_call_response, name="save_call_response"),
]
