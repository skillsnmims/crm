from django.db import models
from django.db.models import Count


class Branch(models.Model):

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_agents_count(self):
        return self.team_set.aggregate(Count("agent"))['agent__count']

    @property
    def get_teams_count(self):
        return self.team_set.count()
