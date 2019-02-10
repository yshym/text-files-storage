from django.forms.widgets import Widget, FileInput


class CustomFileUpload(FileInput):
    template_name = 'widgets/custom_file_upload.html'
