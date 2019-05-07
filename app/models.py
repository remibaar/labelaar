from django.db import models


class Label(models.Model):
    title = models.CharField(max_length=128)
    color = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentImport(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=128, blank=True)

    def number_of_documents(self):
        return self.documents.count()

    def __str__(self):
        return str(self.datetime)+' - '+self.filename


class Document(models.Model):
    text = models.TextField()
    labels = models.ManyToManyField(Label, blank=True)
    annotated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document_import = models.ForeignKey(DocumentImport, related_name='documents', on_delete=models.CASCADE, blank=True, null=True)

    def shortened_text(self, length=50, suffix='...'):
        text = str(self.text)

        if len(text) <= length:
            return text

        new_length = length-len(suffix)
        return text[:new_length]+suffix

    def __str__(self):
        return self.shortened_text()
