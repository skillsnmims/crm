from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.views import get_branch_id
from agents.forms import AgentCreateForm, AgentUpdateForm
from agents.models import Agent
from branches.models import Branch


class AgentListView(LoginRequiredMixin, ListView):

    model = Agent
    template_name = "agents/list.html"
    context_object_name = "agents"

    def get_queryset(self):
        qs = super().get_queryset()
        branch_id = get_branch_id(self.request)
        return qs.filter(team__branch_id=branch_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        branch_id = get_branch_id(self.request)
        branch = Branch.objects.get(id=branch_id)
        context['teams'] = branch.team_set.all()
        return context


class AgentCreateView(LoginRequiredMixin, CreateView):

    model = Agent
    template_name = "agents/create.html"
    form_class = AgentCreateForm
    success_url = reverse_lazy("agents:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user_type = "AG"
        user = form.save()
        Agent.objects.create(user=user,
                             name=form.cleaned_data['name'],
                             agent_id=form.cleaned_data['agent_id'],
                             team=form.cleaned_data['team'])
        messages.success(self.request, "Agent Created Successfully!")
        return super().form_valid(form)


class AgentDetailView(LoginRequiredMixin, DetailView):

    model = Agent
    slug_url_kwarg = "id"
    slug_field = "id"
    context_object_name = "agent"
    template_name = "agents/detail.html"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.team.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to agent!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        agent = super().get_object()
        agent_calls = agent.call_set.all().order_by('-created_on')
        dates = agent_calls.values_list("created_on", flat=True)
        date_progress = {}
        for date in dates:
            progress = {
                "leads": agent_calls.filter(created_on__date=date, response="SC").count(),
                "calls": agent_calls.filter(created_on__date=date).count()
            }
            date_progress[date.date] = progress
        context['all_calls'] = agent_calls.count()
        context['all_leads'] = agent_calls.filter(response="SC").count()
        context['date_progress'] = date_progress
        return context


class AgentUpdateView(LoginRequiredMixin, UpdateView):

    model = Agent
    template_name = "agents/update.html"
    form_class = AgentUpdateForm
    success_url = reverse_lazy("agents:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Agent Created Successfully!")
        if form.cleaned_data['password'] != "":
            form.instance.user.set_password(form.cleaned_data['password'])
            form.instance.user.save()
        return super().form_valid(form)


class AgentDeleteView(LoginRequiredMixin, DeleteView):

    model = Agent
    # template_name = "agents/delete.html"
    # form_class = AgentUpdateForm
    success_url = reverse_lazy("agents:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.team.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to agent!")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Agent Deleted Successfully!")
        return super().delete(request, *args, **kwargs)

