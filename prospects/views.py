from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
import csv
from accounts.views import get_branch_id
from prospects.forms import ProspectListCreateForm
from prospects.models import ProspectList, Prospect
import os


class ProspectListListView(LoginRequiredMixin, ListView):

    model = ProspectList
    template_name = "prospects/list.html"
    context_object_name = "prospect_lists"
    ordering = "-id"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_visitor:
            return qs.filter(visitor=self.request.user.visitor)
        branch_id = get_branch_id(self.request)
        return qs.filter(branch_id=branch_id)


class ProspectListCreateView(LoginRequiredMixin, CreateView):

    model = ProspectList
    template_name = "prospects/create.html"
    form_class = ProspectListCreateForm
    success_url = reverse_lazy("prospects:list")

    def form_valid(self, form):
        if self.request.user.is_visitor:
            branch_id = self.request.user.visitor.branch_id
            form.instance.visitor = self.request.user.visitor
        else:
            branch_id = get_branch_id(self.request)
        form.instance.branch_id = branch_id
        prospect_list = form.save()
        success, missing_columns, no_records = create_prospects_from_list(prospect_list)
        if success:
            messages.success(self.request, "Data List ( {} records )Created Successfully!".format(success))
            return redirect(self.success_url)
        else:
            if missing_columns:
                form.add_error(None, "Missing Columns in file : {}".format(missing_columns))
            else:
                form.add_error(None, "No records found in file.")
            prospect_list.delete()
            return super().form_invalid(form)


class ProspectListDetailView(LoginRequiredMixin, DetailView):

    model = ProspectList
    template_name = "prospects/detail.html"
    context_object_name = "prospect_list"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user.is_visitor and obj.visitor == self.request.user.visitor:
            return obj
        elif self.request.user.is_super_admin or self.request.user.is_branch_admin:
            branch_id = get_branch_id(self.request)
            if obj.branch_id == branch_id:
                return obj
        raise Http404("No access to data list!")


class ProspectListDeleteView(LoginRequiredMixin, DeleteView):

    model = ProspectList
    success_url = reverse_lazy("prospects:list")
    slug_url_kwarg = "id"
    slug_field = "id"

    def get_object(self, queryset=None):
        branch_id = get_branch_id(self.request)
        obj = super().get_object()
        if obj.branch_id == branch_id:
            if obj.campaign is not None:
                raise Http404("Data List is assigned to campaign!\nCannot delete now.")
            return obj
        else:
            raise Http404("No access to data list!")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Campaign Deleted Successfully!")
        return super().delete(request, *args, **kwargs)


def create_prospects_from_list(prospect_list):
    file = prospect_list.csv_file
    with open(file.path, encoding="latin1") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        missing_columns = check_file_header(csv_reader)
        if len(missing_columns) == 0:
            all_prospects = []
            for row in csv_reader:
                all_prospects.append(get_prospect_instance(row, prospect_list.id))
            if len(all_prospects) > 0:
                Prospect.objects.bulk_create(all_prospects)
                return len(all_prospects), missing_columns, False
            else:
                return False, False, False
        else:
            return False, missing_columns, False


CSV_CONSTANT_COLUMNS = ['TIMEZONE', 'FIRST-NAME', 'LAST-NAME', 'PHONE', 'EMAIL', 'INDUSTRY', 'COMPANY', 'EMP-RANGE',
                        'WEBSITE', 'CITY', 'COUNTRY', 'ZIP-CODE', 'ADDRESS-1', 'ADDRESS-2']


def check_file_header(csv_reader):
    header = csv_reader.fieldnames
    print(header)
    missing_columns = []
    for column in CSV_CONSTANT_COLUMNS:
        if column not in header:
            missing_columns.append(column)
    return missing_columns


def get_prospect_instance(row, pl_id):
    prospect = Prospect(
        timezone=str(row.get('TIMEZONE' or "-")).upper() if row.get('TIMEZONE' or None) is not None else None,
        first_name=row.get('FIRST-NAME' or "-"),
        last_name=row.get('LAST-NAME' or "-"),
        phone=row.get('PHONE' or "-"),
        email=row.get('EMAIL' or "-"),
        industry=row.get('INDUSTRY' or "-"),
        company=row.get('COMPANY' or "-"),
        c_emp_range=row.get('EMP-RANGE' or "-"),
        c_website=row.get('WEBSITE' or "-"),
        city=row.get('CITY' or "-"),
        country=row.get('COUNTRY' or "-"),
        zip_code=row.get('ZIP-CODE' or "-"),
        address_1=row.get('ADDRESS-1' or "-"),
        address_2=row.get('ADDRESS-2' or "-"),
        job_title=row.get('JOB-TITLE' or '-'),
        prospect_list_id=pl_id
    )
    return prospect


@login_required
def format_file_download(request):
    try:
        with open(os.path.join(settings.BASE_DIR, "prospects", "file_format.csv"), "rb") as f:
            file_content = f.read()
        response = HttpResponse(file_content, content_type="text/csv")
        response['Content-Disposition'] = 'inline; filename=oceanone-crm-data-format.csv'
        return response
    except:
        return HttpResponse("Unable to process")
