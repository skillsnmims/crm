from django import template

from accounts.views import get_branch_id, get_branch_name
from branches.models import Branch

register = template.Library()


@register.simple_tag
def get_campaign_team_leads_count(campaign, team):
    return campaign.get_team_leads_count(team)


@register.simple_tag
def get_campaign_team_calls_count(campaign, team):
    return campaign.get_team_calls_count(team)


@register.simple_tag
def get_campaign_agent_leads_count(campaign, agent):
    return campaign.get_agent_leads_count(agent)


@register.simple_tag
def get_campaign_agent_calls_count(campaign, agent):
    return campaign.get_agent_calls_count(agent)


@register.simple_tag
def get_branches():
    return Branch.objects.all()


@register.simple_tag
def get_active_branch_name(request):
    return get_branch_name(request)
