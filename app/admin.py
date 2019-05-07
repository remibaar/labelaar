from django.contrib import admin
from django.utils.html import format_html

from .models import Label, Document, DocumentImport
from .forms import DocumentImportModelForm
from .importer import import_file


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentImport)
class ImportAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'filename', 'description', 'number_of_documents', 'delete_button']
    list_filter = ['datetime', 'filename']
    form = DocumentImportModelForm
    list_display_links = None

    def delete_button(self, obj):
        return format_html('<a class="deletelink" href="/admin/app/documentimport/{}/delete/">Delete</a>', obj.id)

    # def save_form(self, request, form, change):
    #     file = form.cleaned_data.get('file', None)
    #     return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        file = form.cleaned_data.get('file', None)
        column = form.cleaned_data.get('column', None)
        sep = form.cleaned_data.get('sep', None)
        obj.filename = file.name
        super().save_model(request, obj, form, change)

        import_file(obj, file.file,  column, sep)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['shortened_text', 'annotated', 'document_import']
    search_fields = ['text']
    list_filter = ['annotated', 'labels__title', 'document_import']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
