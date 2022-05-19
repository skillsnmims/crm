from django import forms

from prospects.models import ProspectList


class ProspectListCreateForm(forms.ModelForm):

    class Meta:
        model = ProspectList
        fields = ('name', 'csv_file', 'description')
        help_texts = {
            "csv_file": "Only CSV file allowed."
        }
