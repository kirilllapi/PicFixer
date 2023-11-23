from django import forms
from .models import Image

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

class UploadFileForm_M(forms.Form):
    file = forms.FileField(label="Файл")

class UploadFileForm_B(forms.Form):
    file = forms.FileField(label="Файл")