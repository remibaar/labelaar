from django import forms
from app.models import DocumentImport


class DocumentImportModelForm(forms.ModelForm):
    file = forms.FileField()
    column = forms.CharField()
    sep = forms.CharField()
    field_order = ['file', 'description']

    class Meta:
        model = DocumentImport
        fields = ['description']
