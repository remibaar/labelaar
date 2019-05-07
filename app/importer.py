import pandas as pd
from .models import DocumentImport, Document


def import_file(document_import: DocumentImport, file, column, sep=','):
    df = pd.read_csv(file, sep=sep, usecols=[column], warn_bad_lines=True, error_bad_lines=False, encoding='latin1')

    for text in df[column]:
        document = Document()
        document.text = text
        document.document_import = document_import
        document.save()
