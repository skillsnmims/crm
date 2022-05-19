from django.conf.urls import url
from . import views

app_name = "branches"

urlpatterns = [
    url(r"^change/(?P<id>[0-9]+)/$", views.change_branch, name="change_branch"),
    url(r"^$", views.BranchListView.as_view(), name="list"),
    url(r"^chats$", views.ChatView.as_view(), name="chats"),
    url(r"^create/$", views.BranchCreateView.as_view(), name="create"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.BranchDetailView.as_view(), name="detail"),
    url(r"^update/(?P<id>[0-9]+)/$", views.BranchUpdateView.as_view(), name="update"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.BranchDeleteView.as_view(), name="delete"),

    url(r"^admins/list/$", views.BranchAdminListView.as_view(), name="admins_list"),
    url(r"^admins/create/$", views.BranchAdminCreateView.as_view(), name="admins_create"),
    url(r"^admins/delete/(?P<id>[0-9]+)/$", views.BranchAdminDeleteView.as_view(), name="admins_delete"),
    url(r"^admins/update/(?P<id>[0-9]+)/$", views.BranchAdminUpdateView.as_view(), name="admins_update"),

    url(r"^visitors/list/$", views.VisitorListView.as_view(), name="visitors_list"),
    url(r"^visitors/create/$", views.VisitorCreateView.as_view(), name="visitors_create"),
    url(r"^visitors/delete/(?P<id>[0-9]+)/$", views.VisitorDeleteView.as_view(), name="visitors_delete"),
    url(r"^visitors/update/(?P<id>[0-9]+)/$", views.VisitorUpdateView.as_view(), name="visitors_update"),

]
