from socket import fromshare
from django import forms


class UploadForm(forms.Form):
    image_field = forms.ImageField()
