import json
import random
import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from accounts.views import get_branch_id
from calls.models import Call
from calls.serializers import CallSerializer
from campaigns.forms import CampaignCreateForm, CampaignUpdateForm
from campaigns.models import Campaign, CampaignProspect
from crm_timezones.models import TimeZone
from prospects.models import ProspectList


def get_priority_campaign_prospects(campaign):
    priority_campaign_prospects = campaign.campaignprospect_set.all()
    print(campaign.timezone_type)
    if campaign.timezone_type == 'AUTO':
        current_time = timezone.now().time()
        current_timezones = TimeZone.objects.all()
       # if before 00:00 AM exclude else make filter
        priority_campaign_prospects = priority_campaign_prospects.filter(prospect__timezone__in=current_timezones.values_list('name', flat=True))
    elif campaign.timezone_type == 'CUSTOM':
        priority_campaign_prospects = priority_campaign_prospects.filter(prospect__timezone__in=campaign.timezones.all().values_list('name', flat=True))
    return priority_campaign_prospects


def get_prospect_call(agent, campaign):
    print("get prospect call")
    priority_campaign_prospects = get_priority_campaign_prospects(campaign)
    callback_campaign_prospects = priority_campaign_prospects.filter(call_time__lt=timezone.now())
    if callback_campaign_prospects.exists(): #TEMP and False
        all_campaign_prospects = callback_campaign_prospects
        is_callback = True
    else:
        all_campaign_prospects = priority_campaign_prospects.all()
        is_callback = False
    if all_campaign_prospects.count() > 0:
        random_index = random.randint(0, all_campaign_prospects.count() - 1)
        random_campaign_prospect = all_campaign_prospects[random_index]
        prospect = random_campaign_prospect.prospect
        random_campaign_prospect.locked = True
        random_campaign_prospect.delete()
        call = create_campaign_call(agent=agent, prospect=prospect, campaign=campaign)
        return call, is_callback
    else:
        return None, None


def create_campaign_call(agent, prospect, campaign):
    call = Call.objects.create(agent=agent, prospect=prospect, campaign=campaign)
    return call


def update_campaign_data(campaign):
    for prospect_list in campaign.prospectlist_set.all():
        create_campaign_prospects(campaign, prospect_list)
    return True


def create_campaign_prospects(campaign, prospect_list):
    all_objects = []
    for prospect in prospect_list.prospect_set.all():
        if not prospect.campaignprospect_set.filter(campaign=campaign).exists() and not prospect.call_set.filter(campaign=campaign):
            all_objects.append(CampaignProspect(prospect=prospect, campaign=campaign))
    if len(all_objects) > 0:
        CampaignProspect.objects.bulk_create(all_objects)
    return True


class CampaignListView(LoginRequiredMixin, ListView):

    model = Campaign
    template_name = "campaigns/list.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        qs = super().get_queryset()
        branch_id = get_branch_id(self.request)
        return qs.filter(branch_id=branch_id)


class CampaignCreateView(LoginRequiredMixin, CreateView):

    model = Campaign
    template_name = "campaigns/create.html"
    form_class = CampaignCreateForm
    success_url = reverse_lazy("campaigns:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Campaign Created Successfully!")
        branch_id = get_branch_id(self.request)
        form.instance.branch_id = branch_id
        campaign = form.save()
        teams = form.cleaned_data['teams']
        teams.update(campaign=campaign)
        prospect_list = form.cleaned_data['prospect_lists']
        prospect_list.update(campaign=campaign)
        update_campaign_data(campaign)
        return redirect(self.success_url)


class CampaignDetailView(LoginRequiredMixin, DetailView):

    model = Campaign
    template_name = "campaigns/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    context_object_name = "campaign"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to campaign!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        campaign = super().get_object()
        campaign_leads = campaign.call_set.filter(response="SC")
        context['call_leads'] = campaign_leads.count()
        context['campaign_leads'] = campaign_leads
        context['call_connects'] = campaign.get_connects_count
        context['call_fails'] = campaign.get_fails_count
        context['call_callbacks'] = campaign.get_callbacks_count
        context['call_ans_machs'] = campaign.get_ans_machs_count
        context['call_dncs'] = campaign.get_dncs_count
        context['call_wrong_numbers'] = campaign.get_wrong_numbers_count
        context['calls_count'] = campaign.get_calls_count
        return context


class CampaignUpdateView(LoginRequiredMixin, UpdateView):

    model = Campaign
    success_url = reverse_lazy("campaigns:list")
    slug_url_kwarg = "id"
    slug_field = "id"
    form_class = CampaignUpdateForm
    template_name = "campaigns/update.html"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to campaign!")

    def form_valid(self, form):
        messages.success(self.request, "Campaign Updated Successfully!")
        branch_id = get_branch_id(self.request)
        form.instance.branch_id = branch_id
        campaign = form.save()
        teams = form.cleaned_data['teams']
        teams.update(campaign=campaign)
        prospect_list = form.cleaned_data['prospect_lists']
        prospect_list.update(campaign=campaign)
        update_campaign_data(campaign)
        return redirect(self.success_url)


class CampaignDeleteView(LoginRequiredMixin, DeleteView):

    model = Campaign
    success_url = reverse_lazy("campaigns:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to campaign!")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Campaign Deleted Successfully!")
        # return HttpResponse("Deleted!")
        return super().delete(request, *args, **kwargs)


class CampaignDispositionListView(LoginRequiredMixin, ListView):

    model = Campaign
    template_name = "campaigns/dispositions/list.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        qs = super().get_queryset()
        branch_id = get_branch_id(self.request)
        return qs.filter(branch_id=branch_id, status="AC")


class CampaignDispositionDetailView(LoginRequiredMixin, DetailView):

    model = Campaign
    template_name = "campaigns/dispositions/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    context_object_name = "campaign"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            return obj
        else:
            raise Http404("No access to campaign!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        campaign = super().get_object()
        calls = campaign.call_set.exclude(response='').order_by("-id")
        # calls = campaign.call_set.all()
        serializer = CallSerializer(calls, many=True)
        json_data = serializer.data
        context['json_data'] = json.dumps(json_data)
        print(calls.count())
        return context


def campaign_disposition_detail(request):
    calls = Call.objects.all()
    serializer = CallSerializer(calls, many=True)
    return JsonResponse(serializer.data, safe=False)
