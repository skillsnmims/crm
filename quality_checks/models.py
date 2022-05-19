from django.db import models

QC_RESPONSE_CHOICES = (("PN", "Pending"), ("AP", "Approved"), ("RJ", "Rejected"))


class QualityCheck(models.Model):

    call = models.ForeignKey("calls.Call", on_delete=models.CASCADE)
    quality_agent = models.ForeignKey("accounts.QualityAgent", on_delete=models.CASCADE)
    response = models.CharField(max_length=2, choices=QC_RESPONSE_CHOICES, default="PN")
    comment = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.call
