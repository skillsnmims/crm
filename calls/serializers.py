from rest_framework import serializers

from agents.models import Agent
from branches.models import Branch
from calls.models import Call
from campaigns.models import Campaign
from prospects.models import Prospect


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['name']


class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = ['first_name', 'last_name', 'phone', 'email', 'job_title', 'company', 'c_emp_range', 'c_website', 'industry', 'address_1', 'address_2', 'city', 'country', 'zip_code']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name']


class CampaignSerializer(serializers.ModelSerializer):

    branch = BranchSerializer(required=True)

    class Meta:
        model = Campaign
        fields = ['name', 'branch']


class CallSerializer(serializers.ModelSerializer):

    prospect = ProspectSerializer(required=True)
    campaign = CampaignSerializer(required=True)
    # agent = AgentSerializer(required=True)
    created_on = serializers.DateTimeField(format='%d/%m/%Y')
    response = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ['id', 'campaign', 'agent', 'created_on', 'call_duration', 'response', 'comment', 'notes', 'prospect']
        # fields = ['prospect']

    def get_response(self, obj):
        return obj.get_response_display()

    def get_agent(self, obj):
        try:
            return obj.agent.user.email
        except:
            return "N/A"
