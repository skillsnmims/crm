from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from accounts.views import get_branch_id
from branches.forms import BranchCreateForm, BranchUpdateForm
from branches.models import Branch
from django.contrib.auth.mixins import UserPassesTestMixin

from calls.models import Call
from teams.forms import TeamCreateForm, TeamUpdateForm
from teams.models import Team


class TeamListView(LoginRequiredMixin, ListView):

    model = Team
    template_name = "teams/list.html"
    context_object_name = "teams"

    def get_queryset(self):
        qs = super().get_queryset()
        branch_id = get_branch_id(self.request)
        return qs.filter(branch_id=branch_id)


class TeamCreateView(LoginRequiredMixin, CreateView):

    model = Team
    template_name = "teams/create.html"
    form_class = TeamCreateForm
    success_url = reverse_lazy("teams:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Team Created Successfully!")
        branch_id = get_branch_id(self.request)
        form.instance.branch_id = branch_id
        return super().form_valid(form)


class TeamDetailView(LoginRequiredMixin, DetailView):

    model = Team
    slug_url_kwarg = "id"
    slug_field = "id"
    context_object_name = "team"
    template_name = "teams/detail.html"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to team")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        team = super().get_object()
        team_calls = Call.objects.filter(agent__team=team).order_by('-created_on')
#        dates = team_calls.values_list("created_on", flat=True)
        date_progress = {}
#        for date in dates:
#            progress = {
#                "leads": team_calls.filter(created_on__date=date, response="SC").count(),
#                "calls": team_calls.filter(created_on__date=date).count()
#            }
#            date_progress[date.date] = progress
        context['all_calls'] = team_calls.count()
        context['all_leads'] = team_calls.filter(response="SC").count()
        context['date_progress'] = date_progress
        return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):

    model = Team
    success_url = reverse_lazy("teams:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to team")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Team Deleted Successfully!")
        # return HttpResponse("Deleted!")
        return super().delete(request, *args, **kwargs)


class TeamUpdateView(LoginRequiredMixin, UpdateView):

    model = Team
    template_name = "teams/update.html"
    form_class = TeamUpdateForm
    slug_url_kwarg = "id"
    slug_field = "id"
    context_object_name = "team"
    success_url = reverse_lazy("teams:list")

    def form_valid(self, form):
        messages.success(self.request, "Team Updated Successfully!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
