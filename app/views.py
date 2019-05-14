from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Document, Label
from .utils import get_dict_from_request


@login_required
def label(request):
    if request.method == 'POST':
        label_ids = get_dict_from_request(request, 'label_')
        label_ids = {k: v for k, v in label_ids.items() if v == 1}

        document_id = request.POST['document_id']
        document = Document.objects.get(id=document_id)

        for label_id in label_ids:
            label = Label.objects.get(id=label_id)
            document.labels.add(label)

        document.annotated = True
        document.save()

        return redirect('/label/')

    document = Document.objects.filter(annotated=False).first()
    labels = Label.objects.all()
    guideline = 'Bla die bla die bla'
    context = {
        'document': document,
        'labels': labels,
        'guideline': guideline
    }

    return render(request, 'labelaar/label.html', context)
