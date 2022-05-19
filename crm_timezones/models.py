from django.db import models


class TimeZone(models.Model):

    name = models.CharField(max_length=12)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(default=0)

    from_ist = models.TimeField()
    to_ist = models.TimeField()

    def __str__(self):
        return self.name
