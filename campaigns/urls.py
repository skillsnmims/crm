from django.conf.urls import url
from . import views

app_name = "campaigns"

urlpatterns = [
    url(r"^$", views.CampaignListView.as_view(), name="list"),
    url(r"^create/$", views.CampaignCreateView.as_view(), name="create"),
    url(r"^update/(?P<id>[0-9]+)/$", views.CampaignUpdateView.as_view(), name="update"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.CampaignDeleteView.as_view(), name="delete"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.CampaignDetailView.as_view(), name="detail"),

    url(r"^dispositions/$", views.CampaignDispositionListView.as_view(), name="disposition_list"),
    url(r"^dispositions/detail/(?P<id>[0-9]+)/$", views.CampaignDispositionDetailView.as_view(), name="disposition_detail"),
]
