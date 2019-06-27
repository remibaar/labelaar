from django.contrib import admin
from django.utils.html import format_html
from io import StringIO
from django.http import HttpResponse
from functools import update_wrapper

from .models import Label, Document, DocumentImport
from .forms import DocumentImportModelForm
from .importer import import_file, export


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
    change_list_template = 'admin/document_change_list.html'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        url_patterns = super().get_urls()
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        url_patterns = [
            path('export/', wrap(self.export_view), name='%s_%s_export' % info)
        ] + url_patterns

        return url_patterns

    def export_view(self, request, form_url='', extra_context=None):
        bytes_io = StringIO()
        export(bytes_io)
        bytes_io.seek(0)
        response = HttpResponse(bytes_io.read(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=labelaar_export.csv'
        return response
