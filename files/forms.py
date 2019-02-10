from django import forms

from .models import File
from .widgets import CustomFileUpload


class FileForm(forms.ModelForm):
    source = forms.FileField(
        widget=CustomFileUpload()
    )

    class Meta:
        model = File
        fields = (
            'name',
            'source',
            'description'
        )
