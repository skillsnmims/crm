from django import forms

from accounts.views import get_branch
from campaigns.models import Campaign
from prospects.models import ProspectList
from teams.models import Team


class CampaignCreateForm(forms.ModelForm):

    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.filter(campaign=None), required=False)
    prospect_lists = forms.ModelMultipleChoiceField(queryset=ProspectList.objects.filter(campaign=None), required=False)

    class Meta:
        model = Campaign
        fields = ('campaign_type', 'name', 'asset_name', 'timezone_type', 'timezones', 'questions', 'confirm', 'consent', 'rebuttal', 'status', "teams", 'prospect_lists')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        branch = get_branch(request)
        self.fields['teams'].queryset = branch.team_set.filter(campaign=None)
        self.fields['prospect_lists'].queryset = branch.prospectlist_set.filter(campaign=None)


class CampaignUpdateForm(forms.ModelForm):

    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.filter(campaign=None), required=False)
    prospect_lists = forms.ModelMultipleChoiceField(queryset=ProspectList.objects.filter(campaign=None), required=False)

    class Meta:
        model = Campaign
        fields = ('campaign_type', 'name', 'asset_name', 'timezone_type', 'timezones', 'questions', 'confirm', 'consent', 'rebuttal', 'status')
        labels = {
            'teams': "Add Teams",
            'prospect_lists': "Add Data Lists"
        }

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance
            self.fields['campaign_type'].initial = instance.campaign_type
            self.fields['name'].initial = instance.name
            self.fields['asset_name'].initial = instance.asset_name
            self.fields['timezone_type'].initial = instance.timezone_type
            self.fields['timezones'].initial = instance.timezones.all()
            self.fields['consent'].initial = instance.consent
            self.fields['confirm'].initial = instance.confirm
            self.fields['questions'].initial = instance.questions
            self.fields['rebuttal'].initial = instance.rebuttal
            self.fields['status'].initial = instance.status
            self.fields['teams'].queryset = instance.branch.team_set.filter(campaign=None)
            self.fields['prospect_lists'].queryset = instance.branch.prospectlist_set.filter(campaign=None)
            self.fields['teams'].label = "Add Teams To Campaign"
            self.fields['prospect_lists'].label = "Add Data Lists To Campaign"
