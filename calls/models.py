from django.core.validators import MinValueValidator
from django.db import models



CALL_RESPONSE_CHOICES = (
    ("SC", "Lead"),
    ("CN", "Connect"),
    ("FL", "Failure"),
    ("DNC", "Do Not Call"),
    ("AM", "Answering Machine"),
    ("CB", "Callback"),
    ("WN", "Wrong Number"),

    ("DM_FP", "Follow Up"),
    ("DM_CL", "Close"),
    ("DM_NE", "Not Eligible"),
    ("DM_NI", "Not Interested"),
    ("DM_BD", "Bad Contact"),
    ("DM_WN", "Domestic - Wrong No"),
    ("DM_LS", "Low Salary"),
    ("DM_HI", "Health Insurance"),
    ("DM_LI", "Life Insurance"),
    ("DM_PL", "Personal Loan"),
    ("DM_HL", "Home Loan"),
    ("DM_RG", "Ringing"),

)


class Call(models.Model):

    agent = models.ForeignKey("agents.Agent", on_delete=models.SET_NULL, blank=True, null=True)
    prospect = models.ForeignKey("prospects.Prospect", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)
    response = models.CharField(max_length=2, choices=CALL_RESPONSE_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    comment = models.CharField(max_length=64, blank=True)
    call_duration = models.FloatField(default=0.0, validators=[MinValueValidator(limit_value=0.0)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.prospect, self.campaign)
