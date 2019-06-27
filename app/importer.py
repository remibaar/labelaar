import pandas as pd
from .models import DocumentImport, Document


def import_file(document_import: DocumentImport, file, column, sep=','):
    df = pd.read_csv(file, sep=sep, usecols=[column], warn_bad_lines=True, error_bad_lines=False, encoding='latin1')

    for text in df[column]:
        document = Document()
        document.text = text
        document.document_import = document_import
        document.save()


def export(io_buffer):
    documents = Document.objects.all()
    records = []
    columns = ['id', 'text', 'annotated', 'labels', 'label_ids']
    for d in documents:
        labels = d.labels.all()
        records.append([
            d.id,
            d.text,
            d.annotated,
            ','.join([l.title for l in labels]),
            ','.join([str(l.id) for l in labels]),
        ])
    df = pd.DataFrame(records, columns=columns)
    df.to_csv(io_buffer, index=False)
