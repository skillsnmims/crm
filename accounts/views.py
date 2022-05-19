from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# class UserSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
#     def test_func(self):
#         return test_settings(self.request.user)
#
#     def get_login_url(self):
#         if not self.request.user.is_authenticated():
#             return super(UserSettingsView, self).get_login_url()
#         else:
#             return '/accounts/usertype/'
from branches.models import Branch


def get_branch_id(request):
    if request.user.is_super_admin:
        if "current_branch_id" in request.session:
            branch_id = request.session['current_branch_id']
        else:
            branch = Branch.objects.first()
            request.session['current_branch_id'] = branch.id
            request.session['current_branch_name'] = branch.name
            request.session.modified = True
            branch_id = branch.id
    else:
        branch_id = request.user.branchadmin.branch.id
    return branch_id


def get_branch_name(request):
    if request.user.is_super_admin:
        if "current_branch_name" in request.session:
            branch_name = request.session['current_branch_name']
        else:
            branch = Branch.objects.first()
            request.session['current_branch_id'] = branch.id
            request.session['current_branch_name'] = branch.name
            request.session.modified = True
            branch_name = branch.name
    else:
        branch_name = request.user.branchadmin.branch.name
    return branch_name


def get_branch(request):
    if request.user.is_super_admin:
        if "current_branch_id" in request.session:
            branch_id = request.session['current_branch_id']
            branch = Branch.objects.get(id=branch_id)
        else:
            branch = Branch.objects.first()
            request.session['current_branch_id'] = branch.id
            request.session['current_branch_name'] = branch.name
            request.session.modified = True
            branch = branch
    else:
        branch = request.user.branchadmin.branch
    return branch


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password has been changed successfully!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request, "Please fill valid details")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
