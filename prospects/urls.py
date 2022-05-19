from django.conf.urls import url
from . import views

app_name = "prospects"

urlpatterns = [
    url(r"^$", views.ProspectListListView.as_view(), name="list"),
    url(r"^format-file/download/$", views.format_file_download, name="format_file_download"),
    url(r"^create/$", views.ProspectListCreateView.as_view(), name="create"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.ProspectListDeleteView.as_view(), name="delete"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.ProspectListDetailView.as_view(), name="detail"),
]
