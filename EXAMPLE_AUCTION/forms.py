from django import forms
from django.forms import ModelForm
from EXAMPLE_AUCTION.models import Document, DocumentType

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['type', 'name', 'path', 'last_modified', 'prioritet']
