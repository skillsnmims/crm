from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView, DeleteView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from calls.models import Call
from campaigns.models import CampaignProspect
from campaigns.views import get_prospect_call, create_campaign_call


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "portal/dashboard.html"

#
# @login_required
# def calling_page(request):
#     if request.user.is_super_admin or request.user.is_branch_admin:
#         return redirect("portal:dashboard")
#     agent = request.user.agent
#     if request.method == "POST":
#         call_id = request.POST['call_id']
#         call_response = request.POST['call_response']
#         call = Call.objects.get(id=call_id, agent=agent)
#         if call.response == "":
#             call.response = call_response
#             call.save()
#             if call_response == "SC":
#                 call.campaign.leads_count += F('leads_count') + 1
#             elif calling_page == "CB":
#                 CampaignProspect.objects.create(campaign=call.campaign, prospect=call.prospect, call_time=timezone.now() + timezone.timedelta(hours=settings.DEFAULT_CALLBACK_GAP))
#     campaign = agent.team.campaign
#     agent_pending_calls = agent.call_set.filter(response="")
#     if agent_pending_calls.exists():
#         call = agent_pending_calls.first()
#         is_pending = True
#         is_callback = False
#     else:
#         call, is_callback = get_prospect_call(agent=agent, campaign=campaign)
#         is_pending = False
#     context = {"call": call, "campaign": campaign, "is_pending": is_pending, "is_callback": is_callback}
#     return render(request, "portal/calling_page.html", context=context)


@login_required
@csrf_exempt
def calling_page(request):
    team = None
    if request.user.is_super_admin or request.user.is_branch_admin:
        return redirect("portal:dashboard")
    agent = request.user.agent
    if request.method == "POST":
        call_id = request.POST['call_id']
        call_response = request.POST['call_response']
        call = Call.objects.get(id=call_id, agent=agent)
        if call.response == "":
            call.response = call_response
            call.notes = request.POST.get('call_notes', '')
            call.comment = request.POST.get('call_comment', '')
            print("call.comment : ", call.comment)
            call.save()
            print(call.comment)
            if call_response == "SC":
                call.campaign.leads_count += F('leads_count') + 1
            elif calling_page == "CB":
                CampaignProspect.objects.create(campaign=call.campaign, prospect=call.prospect, call_time=timezone.now() + timezone.timedelta(hours=settings.DEFAULT_CALLBACK_GAP))
    agent_pending_calls = agent.call_set.filter(response="")
    if agent_pending_calls.exists():
        call = agent_pending_calls.first()
        campaign = call.campaign
        is_pending = True
        is_callback = False
    else:
        team = agent.team
        if team is not None:
            campaign = agent.team.campaign
            print(campaign)
            if campaign is not None:
                call, is_callback = get_prospect_call(agent=agent, campaign=campaign)
                is_pending = False
            else:
                call = None
                is_pending = None
                is_callback = None
        else:
            call = None
            is_pending = None
            is_callback = None
            campaign = None
    if request.method == "POST":
        context = {"has_call": False, "call": {}, "campaign": campaign.id, "is_pending": is_pending, "is_callback": is_callback,
                   "team": team.id}
        if call is not None:
            context['has_call'] = True
            context['call'] = {
                'first_name': call.prospect.first_name,
                'last_name': call.prospect.last_name,
                'company': call.prospect.company,
                'phone': call.prospect.get_formatted_phone(),
                'website': call.prospect.c_website,
                'email': call.prospect.email,
                'emp_range': call.prospect.c_emp_range,
                'job_title': call.prospect.job_title,
                'industry': call.prospect.industry,
                'address': call.prospect.address_1,
                'call_id': call.id,
            }
        return JsonResponse(context, safe=True)
    else:
        context = {"call": call, "campaign": campaign, "is_pending": is_pending, "is_callback": is_callback, "team": team}
        return render(request, "portal/calling_page.html", context=context)



#
# @login_required
# def calling_page(request):
#     team = None
#     if request.user.is_super_admin or request.user.is_branch_admin:
#         return redirect("portal:dashboard")
#     agent = request.user.agent
#     if request.method == "POST":
# #        print(request.POST, "----------------------------"*50)
#         call_id = request.POST['call_id']
#         call_response = request.POST['call_response']
#         call = Call.objects.get(id=call_id, agent=agent)
#         if call.response == "":
#             call.response = call_response
#             call.notes = request.POST.get('call_notes', '')
#             call.comment = request.POST.get('call_comment', '')
#             print("call.comment : ", call.comment)
#             call.save()
#             print(call.comment)
#             if call_response == "SC":
#                 call.campaign.leads_count += F('leads_count') + 1
#             elif calling_page == "CB":
#                 CampaignProspect.objects.create(campaign=call.campaign, prospect=call.prospect, call_time=timezone.now() + timezone.timedelta(hours=settings.DEFAULT_CALLBACK_GAP))
#     agent_pending_calls = agent.call_set.filter(response="")
#     if agent_pending_calls.exists():
#         call = agent_pending_calls.first()
#         campaign = call.campaign
#         is_pending = True
#         is_callback = False
#     else:
#         team = agent.team
#         if team is not None:
#             campaign = agent.team.campaign
#             print(campaign)
#             if campaign is not None:
#                 call, is_callback = get_prospect_call(agent=agent, campaign=campaign)
#                 is_pending = False
#             else:
#                 call = None
#                 is_pending = None
#                 is_callback = None
#         else:
#             call = None
#             is_pending = None
#             is_callback = None
#             campaign = None
#     context = {"call": call, "campaign": campaign, "is_pending": is_pending, "is_callback": is_callback, "team": team}
#     return render(request, "portal/calling_page.html", context=context)
