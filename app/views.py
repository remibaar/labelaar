from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Document, Label


@login_required
def label(request):
    document = Document.objects.first()
    labels = Label.objects.all()
    guideline = 'Bla die bla die bla'
    context = {
        'document': document,
        'labels': labels,
        'guideline': guideline
    }
    return render(request, 'labelaar/label.html', context)
