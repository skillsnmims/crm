from django.core.validators import FileExtensionValidator
from django.db import models


EMP_RANGE_CHOICES = (
    ("1-10", "1 to 10"),
    ("11-50", "11 to 50"),
    ("51-200", "51 to 200"),
    ("201-500", "201 to 500"),
    ("501-1000", "501 to 1000"),
    ("1001-5000", "1001 to 5000"),
    ("5001-10000", "5001 to 10000"),
    ("10000+", "10000+"),
)


class Prospect(models.Model):

    timezone = models.CharField(max_length=12, blank=True, null=True)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)

    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=128, blank=True)

    job_title = models.CharField(max_length=64, blank=True)

    company = models.CharField(max_length=128, blank=True)
    c_emp_range = models.CharField(verbose_name="Employee Range", max_length=32, blank=True)
    c_website = models.CharField(verbose_name="Website", max_length=128, blank=True, null=True)

    industry = models.CharField(max_length=128, blank=True)
    address_1 = models.CharField(max_length=96, blank=True)
    address_2 = models.CharField(max_length=96, blank=True)
    city = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    prospect_list = models.ForeignKey("prospects.ProspectList", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_formatted_phone(self):
        return self.phone.replace('.', '').replace('(', '').replace('(', '').replace('-', '')



class ProspectList(models.Model):

    visitor = models.ForeignKey("accounts.Visitor", on_delete=models.SET_NULL, blank=True, null=True)
    csv_file = models.FileField(upload_to="campaigns/csv_files/", validators=[FileExtensionValidator(allowed_extensions=['csv', ]), ])

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_data_count(self):
        return self.prospect_set.count()

