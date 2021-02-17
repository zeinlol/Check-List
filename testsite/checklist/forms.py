from django import forms
from .models import CheckList


class ListForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ["name",  "description", "completed", "date"]