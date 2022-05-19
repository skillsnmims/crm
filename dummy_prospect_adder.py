import random
import string

from prospects.models import Prospect

prospect_instances = [Prospect(first_name=random.choice(string.ascii_lowercase), phone=random.randint(10000, 99999), prospect_list_id=1) for _ in range(10000)]
Prospect.objects.bulk_create(prospect_instances)


from campaigns.models import *
from prospects.models import *
from campaigns.views import create_campaign_prospects

campaign = Campaign.objects.first()
prospect_list = campaign.prospectlist_set.first()

create_campaign_prospects(campaign=campaign, prospect_list=prospect_list)
