from django.db import models
from django.db.models.signals import post_save, post_delete


class Agent(models.Model):

    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    agent_id = models.CharField(max_length=32, unique=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"


def delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


post_delete.connect(delete_user, sender=Agent)



