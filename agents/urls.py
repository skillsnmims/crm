from django.conf.urls import url
from . import views

app_name = "agents"

urlpatterns = [
    url(r"^$", views.AgentListView.as_view(), name="list"),
    url(r"^create/$", views.AgentCreateView.as_view(), name="create"),
    url(r"^update/(?P<id>[0-9]+)/$", views.AgentUpdateView.as_view(), name="update"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.AgentDetailView.as_view(), name="detail"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.AgentDeleteView.as_view(), name="delete")
]
