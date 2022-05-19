from django.contrib.auth.forms import UserCreationForm

from branches.models import Branch
from django import forms
from accounts.models import BranchAdmin, User, Visitor
from accounts.validators import password_validator


class BranchCreateForm(forms.ModelForm):

    admins = forms.ModelMultipleChoiceField(queryset=BranchAdmin.objects.filter(branch=None), required=False)

    class Meta:
        model = Branch
        fields = ("name", "description", "admins")


class BranchUpdateForm(forms.ModelForm):

    class Meta:
        model = Branch
        fields = ("name", "description")
    #
    # def __init__(self, instance=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if instance is not None:
    #         self.instance = instance
    #         self.fields['admins'].initial = list(instance.branchadmin_set.values_list('id', flat=True))
    #         self.fields['name'].initial = instance.name
    #         self.fields['description'].initial = instance.description


class BranchAdminUpdateForm(forms.ModelForm):

    email = forms.EmailField(disabled=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), required=False, validators=[password_validator])

    class Meta:
        model = BranchAdmin
        fields = ("email", "first_name", "last_name", "branch", "password")

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance
            self.fields['email'].initial = instance.user.email
            self.fields['first_name'].initial = instance.first_name
            self.fields['last_name'].initial = instance.last_name
            self.fields['branch'].initial = instance.branch


class BranchAdminCreateForm(UserCreationForm):

    first_name = forms.CharField(max_length=64, widget=forms.TextInput(), required=True)
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(), required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'branch')


class VisitorCreateForm(UserCreationForm):

    first_name = forms.CharField(max_length=64, widget=forms.TextInput(), required=True)
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(), required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'branch')


class VisitorUpdateForm(forms.ModelForm):

    email = forms.EmailField(disabled=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), required=False, validators=[password_validator])

    class Meta:
        model = Visitor
        fields = ("email", "first_name", "last_name", "branch", "password")

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance
            self.fields['email'].initial = instance.user.email
            self.fields['first_name'].initial = instance.first_name
            self.fields['last_name'].initial = instance.last_name
            self.fields['branch'].initial = instance.branch

