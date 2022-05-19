from django.contrib import admin
from accounts.models import BranchAdmin, User, Visitor, QualityAgent
from agents.models import Agent
from branches.models import Branch
from calls.models import Call
from campaigns.models import Campaign, CampaignProspect, CampaignTeam
from prospects.models import Prospect, ProspectList
from teams.models import Team


admin.site.site_header = "Oceanone CRM"
admin.site.site_title = "Oceanone CRM"

admin.site.register(Branch)
admin.site.register(Campaign)
admin.site.register(BranchAdmin)
admin.site.register(Team)
admin.site.register(Agent)
admin.site.register(User)
admin.site.register(Call)
admin.site.register(QualityAgent)
admin.site.register(Visitor)
admin.site.register(Prospect)
admin.site.register(ProspectList)
admin.site.register(CampaignTeam)
admin.site.register(CampaignProspect)

