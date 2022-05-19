from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('amt-admin/', admin.site.urls),
    url(r"", include("portal.urls", namespace="portal")),
    url(r"^branches/", include("branches.urls", namespace="branches")),
    url(r"^agents/", include("agents.urls", namespace="agents")),
    url(r"^teams/", include("teams.urls", namespace="teams")),
    url(r"^accounts/", include("accounts.urls.urls", namespace="accounts")),
    url(r"^campaigns/", include("campaigns.urls", namespace="campaigns")),
    url(r"^prospects/", include("prospects.urls", namespace="prospects"))
]
