from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError
from accounts.models import User
from accounts.validators import password_validator
from accounts.views import get_branch
from agents.models import Agent


# class AgentCreateForm(forms.ModelForm):
#
#     class Meta:
#         model = Agent
#         fields = ('first_name', 'last_name', 'agent_id', 'team')
from teams.models import Team


class AgentCreateForm(UserCreationForm):

    name = forms.CharField(max_length=128, widget=forms.TextInput(), required=True)
    agent_id = forms.CharField(max_length=32, widget=forms.TextInput(), required=True)
    team = forms.ModelChoiceField(queryset=None, required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'agent_id', 'team')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = get_branch(request).team_set.all()
        self.fields['team'].queryset = qs

    def clean_agent_id(self):
        if Agent.objects.filter(agent_id=self.cleaned_data['agent_id']).exists():
            raise ValidationError("Agent id already exists!")
        return self.cleaned_data['agent_id']


class AgentUpdateForm(forms.ModelForm):

    email = forms.EmailField(disabled=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), required=False, validators=[password_validator])

    class Meta:
        model = Agent
        fields = ("email", "name", "agent_id", "team", "password")

    # def clean_agent_id(self):
    #
    #     if Agent.objects.filter(agent_id=self.cleaned_data['agent_id']).exclude().exists():
    #         raise ValidationError("Agent id already exists!")
    #     return self.cleaned_data['agent_id']

    def __init__(self, request, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = get_branch(request).team_set.all()
        self.fields['team'].queryset = qs
        if instance is not None:
            self.instance = instance
            self.fields['email'].initial = instance.user.email
            self.fields['name'].initial = instance.name
            self.fields['agent_id'].initial = instance.agent_id
            self.fields['team'].initial = instance.team
