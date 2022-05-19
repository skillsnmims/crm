from django.db import models


class Team(models.Model):

    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def get_agents_count(self):
        return self.agent_set.count()
