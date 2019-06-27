from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import File, FileTag
from .widgets import CustomFileUpload

class FileUploadForm(forms.ModelForm):

    class Meta:
        model = File
        fields = (
            'name',
            'source',
            'description',
            'tags',
        )
        widgets = {
            'source': CustomFileUpload,
            'tags': Select2MultipleWidget,
        }


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
            'tags',
        )
        widgets = {
            'tags': Select2MultipleWidget
        }


class FileEditForm(forms.ModelForm):

    class Meta:
        model = File
        fields = (
            'name',
            'description',
            'text',
            'tags',
        )
        widgets = {
            'tags': Select2MultipleWidget
        }


