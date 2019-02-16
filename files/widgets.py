from django.forms.widgets import Widget, FileInput, SelectMultiple


class CustomFileUpload(FileInput):
    template_name = 'widgets/custom_file_upload.html'


class CustomMultipleChoice(SelectMultiple):
    template_name = 'widgets/custom_select_multiple.html'
    option_template_name = 'widgets/custom_select_multiple_option.html'
