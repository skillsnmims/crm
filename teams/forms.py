from django import forms

from accounts.views import get_branch
from branches.models import Branch
from teams.models import Team


class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name', 'description', 'campaign')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = get_branch(request).campaign_set.all()
        self.fields['campaign'].queryset = qs


class TeamUpdateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name', 'description', 'campaign', 'branch')

    def __init__(self, request, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description
            self.fields['campaign'].initial = instance.campaign
            self.fields['branch'].initial = instance.branch
            self.fields['campaign'].queryset = instance.branch.campaign_set.all()
            if not request.user.is_super_admin:
                self.fields['branch'].queryset = Branch.objects.filter(id=instance.branch.id)

