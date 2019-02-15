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
            'description',
        )


class FileCreateForm(forms.ModelForm):
    EXTS = (
        ('.md', 'Markdown'),
        ('.txt', 'Text'),
    )
    text_format = forms.ChoiceField(choices=EXTS)

    class Meta:
        model = File
        fields = (
            'name',
            'description',
            'text',
        )
