from django.db import models
from django.utils import timezone

from django.conf import settings

AGENT_STATUS_CHOICES = (
    ("OF", "Offline"),
    ("ON", "Online"),
    ("BR", "Break"),
)


class AgentActivity(models.Model):
    channel_name = models.CharField(max_length=128)

    agent = models.OneToOneField("agents.Agent", on_delete=models.CASCADE, unique=True)
    status = models.CharField(max_length=4, choices=AGENT_STATUS_CHOICES)
    comment = models.CharField(max_length=128, blank=True, null=True)

    last_seen = models.DateTimeField()
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.agent, self.get_status_display())

    def get_last_seen(self):
        if self.last_seen.date() == timezone.now().date():
            return self.last_seen.strftime(settings.STANDARD_TIME_FORMAT)
        else:
            return self.last_seen.strftime(settings.STANDARD_DATETIME_FORMAT)

    class Meta:
        verbose_name = "Agent Activity"
        verbose_name_plural = "Agent Activities"
