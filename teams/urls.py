from django.conf.urls import url
from . import views

app_name = "teams"

urlpatterns = [
    url(r"^$", views.TeamListView.as_view(), name="list"),
    url(r"^create/$", views.TeamCreateView.as_view(), name="create"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.TeamDetailView.as_view(), name="detail"),
    url(r"^update/(?P<id>[0-9]+)/$", views.TeamUpdateView.as_view(), name="update"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.TeamDeleteView.as_view(), name="delete")
]
