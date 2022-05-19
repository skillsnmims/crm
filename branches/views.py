from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView

from accounts.views import get_branch_id
from branches.forms import BranchCreateForm, BranchUpdateForm, BranchAdminCreateForm, VisitorCreateForm, \
    VisitorUpdateForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from branches.forms import BranchAdminUpdateForm
from accounts.models import BranchAdmin, Visitor
from branches.models import Branch


class SuperuserRequiredMixin(UserPassesTestMixin):

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        if self.request.user.is_super_admin:
            return True
        else:
            return False

    def handle_no_permission(self):
        if self.raise_exception:
            return HttpResponse("You don't have access to this page!")
        return HttpResponse("You don't have access to this page!")


class BranchListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):

    model = Branch
    template_name = "branches/list.html"
    context_object_name = "branches"



class BranchCreateView(LoginRequiredMixin, CreateView):

    model = Branch
    template_name = "branches/create.html"
    form_class = BranchCreateForm
    success_url = reverse_lazy("branches:list")

    def form_valid(self, form):
        messages.success(self.request, "Branch Created Successfully!")
        return super().form_valid(form)


class BranchDetailView(LoginRequiredMixin, DetailView):

    model = Branch
    slug_url_kwarg = "id"
    slug_field = "id"
    template_name = "branches/detail.html"

    def get(self, request, *args, **kwargs):
        branch = super().get_object()
        set_session_branch(request, branch)
        return super().get(request, *args, **kwargs)


class BranchUpdateView(UpdateView):

    model = Branch
    template_name = "branches/update.html"
    slug_url_kwarg = "id"
    slug_field = "id"
    form_class = BranchUpdateForm
    success_url = reverse_lazy("branches:list")

    def form_valid(self, form):
        messages.success(self.request, "Branch has been updated successfully!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        branch = super().get_object()
        set_session_branch(request, branch)
        return super().get(request, *args, **kwargs)


@login_required
@user_passes_test(lambda u: u.is_super_admin)
def change_branch(request, id):
    branch = get_object_or_404(Branch, id=id)
    set_session_branch(request, branch)
    return redirect("portal:dashboard")


def set_session_branch(request, branch):
    request.session['current_branch_id'] = branch.id
    request.session['current_branch_name'] = branch.name
    request.session.modified = True
    return True


class BranchAdminListView(LoginRequiredMixin, ListView):

    model = BranchAdmin
    template_name = "branches/admins/list.html"
    context_object_name = "branch_admins"


class BranchAdminUpdateView(LoginRequiredMixin, UpdateView):

    model = BranchAdmin
    template_name = "branches/admins/update.html"
    slug_url_kwarg = "id"
    slug_field = "id"
    form_class = BranchAdminUpdateForm
    success_url = reverse_lazy("branches:admins_list")

    def form_valid(self, form):
        messages.success(self.request, "Branch has been updated successfully!")
        if form.cleaned_data['password'] != "":
            form.instance.user.set_password(form.cleaned_data['password'])
            form.instance.user.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        branch = super().get_object().branch
        set_session_branch(request, branch)
        return super().get(request, *args, **kwargs)


class BranchDeleteView(LoginRequiredMixin, DeleteView):

    model = Branch
    success_url = reverse_lazy("branches:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Branch Deleted Successfully!")
        # return HttpResponse("Deleted!")
        return super().delete(request, *args, **kwargs)


class BranchAdminCreateView(LoginRequiredMixin, CreateView):
    model = BranchAdmin
    template_name = "branches/admins/create.html"
    form_class = BranchAdminCreateForm
    success_url = reverse_lazy("branches:admins_list")

    def form_valid(self, form):
        form.instance.user_type = "BA"
        user = form.save()
        BranchAdmin.objects.create(user=user,
                                   first_name=form.cleaned_data['first_name'],
                                   last_name=form.cleaned_data['last_name'],
                                   branch=form.cleaned_data['branch'])
        messages.success(self.request, "Admin Created Successfully!")
        return super().form_valid(form)


class BranchAdminDeleteView(LoginRequiredMixin, DeleteView):

    model = BranchAdmin
    success_url = reverse_lazy("branches:admins_list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Branch Admin Deleted Successfully!")
        # return HttpResponse("Deleted! {}".format(self.get_object().user.email))
        return super().delete(request, *args, **kwargs)


#   VISITOR FOR DATA UPLOADING


class VisitorCreateView(LoginRequiredMixin, CreateView):
    model = Visitor
    template_name = "branches/visitors/create.html"
    form_class = VisitorCreateForm
    success_url = reverse_lazy("branches:visitors_list")

    def form_valid(self, form):
        form.instance.user_type = "VS"
        user = form.save()
        Visitor.objects.create(user=user,
                                   first_name=form.cleaned_data['first_name'],
                                   last_name=form.cleaned_data['last_name'],
                                   branch=form.cleaned_data['branch'])
        messages.success(self.request, "Visitor Created Successfully!")
        return super().form_valid(form)


class VisitorDeleteView(LoginRequiredMixin, DeleteView):

    model = Visitor
    success_url = reverse_lazy("branches:visitors_list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Visitor Deleted Successfully!")
        # return HttpResponse("Deleted! {}".format(self.get_object().user.email))
        return super().delete(request, *args, **kwargs)


class VisitorListView(LoginRequiredMixin, ListView):

    model = Visitor
    template_name = "branches/visitors/list.html"
    context_object_name = "visitors"


class VisitorUpdateView(LoginRequiredMixin, UpdateView):

    model = Visitor
    template_name = "branches/visitors/update.html"
    slug_url_kwarg = "id"
    slug_field = "id"
    form_class = VisitorUpdateForm
    success_url = reverse_lazy("branches:visitors_list")

    def form_valid(self, form):
        messages.success(self.request, "Visitor has been updated successfully!")
        if form.cleaned_data['password'] != "":
            form.instance.user.set_password(form.cleaned_data['password'])
            form.instance.user.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        branch = super().get_object().branch
        set_session_branch(request, branch)
        return super().get(request, *args, **kwargs)


class ChatView(LoginRequiredMixin, TemplateView):

    template_name = "branches/admins/chat.html"
