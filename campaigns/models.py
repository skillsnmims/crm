from django.db import models
from django.db.models import Sum, Count

from calls.models import Call

CAMPAIGN_STATUS_CHOICES = (("AC", "Active"), ("IN", "Inactive"))

TIMEZONE_TYPE_CHOICES = (('ALL', 'All Data (with blanks)'), ('AUTO', 'Auto (by current indian time)'), ('CUSTOM', 'Custom (Only Selected)'))
CAMPAIGN_TYPE_CHOICES = (('IN', 'International'), ('DM', 'Domestic'))


class Campaign(models.Model):

    timezone_type = models.CharField(max_length=12, choices=TIMEZONE_TYPE_CHOICES, default='ALL')
    timezones = models.ManyToManyField('crm_timezones.TimeZone', blank=True, null=True)

    campaign_type = models.CharField(max_length=2, choices=CAMPAIGN_TYPE_CHOICES, default="IN")

    name = models.CharField(max_length=128, unique=True)
    asset_name = models.CharField(max_length=128, default="-")
    timezone_str = models.CharField(verbose_name="Timezone", max_length=64, blank=True, null=True)
    consent = models.TextField()
    questions = models.TextField(verbose_name="Script")
    confirm = models.TextField()
    rebuttal = models.TextField()
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    leads_count = models.PositiveSmallIntegerField(default=0)
    # calls_count = models.PositiveSmallIntegerField(default=0)

    status = models.CharField(max_length=2, choices=CAMPAIGN_STATUS_CHOICES, default="AC")

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = ['name', 'branch']

    @property
    def is_domestic(self):
        return self.campaign_type == 'DM'

    def get_team_leads_count(self, team):
        return self.call_set.filter(agent__team=team, response="SC").count()

    def get_team_calls_count(self, team):
        return self.call_set.filter(agent__team=team).count()

    def get_agent_leads_count(self, agent):
        return self.call_set.filter(agent=agent, response="SC").count()

    def get_agent_calls_count(self, agent):
        return self.call_set.filter(agent=agent).count()

    @property
    def get_agents_count(self):
        return self.team_set.aggregate(Count("agent"))['agent__count']

    @property
    def get_teams_count(self):
        return self.team_set.count()

    @property
    def get_leads_count(self):
        return self.call_set.filter(response="SC").count()

    @property
    def get_connects_count(self):
        return self.call_set.filter(response="CN").count()


    @property
    def get_fails_count(self):
        return self.call_set.filter(response="FL").count()

    @property
    def get_dncs_count(self):
        return self.call_set.filter(response="DNC").count()

    @property
    def get_ans_machs_count(self):
        return self.call_set.filter(response="AM").count()

    @property
    def get_callbacks_count(self):
        return self.call_set.filter(response="CB").count()

    @property
    def get_wrong_numbers_count(self):
        return self.call_set.filter(response="WN").count()

    @property
    def get_calls_count(self):
        return self.call_set.count()

    @property
    def get_remaining_data_count(self):
        return self.campaignprospect_set.count()

    @property
    def get_total_data_count(self):
        return self.prospectlist_set.aggregate(Count("prospect"))['prospect__count']


class CampaignProspectList(models.Model):

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)
    prospect_list = models.ForeignKey("prospects.ProspectList", on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.campaign, self.prospect_list)


class CampaignTeam(models.Model):

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    ended_on = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.campaign, self.team)


class CampaignProspect(models.Model):

    prospect = models.ForeignKey("prospects.Prospect", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)

    call_time = models.DateTimeField(blank=True, null=True)
    """ Currently using for callback instances. """

    def __str__(self):
        return "{} - {}".format(self.prospect, self.campaign)
