from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.utils.encoding import smart_str
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

import os

from .models import File
from .forms import FileForm


class FileListView(generic.ListView):
    model = File
    template_name = 'file_list.djhtml'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('Search')
        if query:
            object_list = self.model.objects.filter(Q(name__icontains = query) |
                                                    Q(description__icontains = query))
        else:
            object_list = self.model.objects.all()
        return object_list


class FileDetailView(generic.DetailView):
    model = File
    template_name = 'file_detail.djhtml'


class FileAnonCreateView(SuccessMessageMixin, generic.edit.CreateView):
    model = File
    fields = (
        'name',
        'description',
        'text',
    )
    template_name = 'file_create.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully created!'
    creation_type = 'Anonymously'

    def form_valid(self, form):
        form.instance.source = SimpleUploadedFile('file.txt', form.instance.text.encode('ascii'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(FileAnonCreateView, self).get_context_data(**kwargs)
        ctx['creation_type'] = self.creation_type
        return ctx


class FileAuthCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = File
    fields = (
        'name',
        'description',
        'text',
    )
    template_name = 'file_create.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully created!'
    login_url = 'login'
    creation_type = 'With your account'

    def form_valid(self, form):
        form.instance.source = SimpleUploadedFile('file.txt', form.instance.text.encode('ascii'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(FileAuthCreateView, self).get_context_data(**kwargs)
        ctx['creation_type'] = self.creation_type
        return ctx



class FileAnonUploadView(SuccessMessageMixin, generic.edit.CreateView):
    form_class = FileForm
    template_name = 'file_upload.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully uploaded!'
    uploading_type = 'Anonymously'

    def get_context_data(self, **kwargs):
        ctx = super(FileAnonUploadView, self).get_context_data(**kwargs)
        ctx['uploading_type'] = self.uploading_type
        return ctx


class FileAuthUploadView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    form_class = FileForm
    template_name = 'file_upload.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully uploaded!'
    login_url = 'login'
    uploading_type = 'With your account'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(FileAuthUploadView, self).get_context_data(**kwargs)
        ctx['uploading_type'] = self.uploading_type
        return ctx


class FileEditView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = File
    fields = (
        'name',
        'description',
        'text',
    )
    template_name = 'file_edit.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully edited!'
    login_url = 'login'

    def form_valid(self, form):
        file_obj = File.objects.get(slug=str(self.kwargs['slug']))
        form.instance.source = SimpleUploadedFile(f'{settings.MEDIA_ROOT}/{form.instance.name}/{form.instance.name}{file_obj.get_ext()}', form.instance.text.encode('utf-8'))
        file_obj.remove_file()
        return super().form_valid(form)


class FileDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.DeleteView):
    model = File
    template_name = 'file_delete.djhtml'
    success_url = reverse_lazy('file_list')
    success_message = 'File was successfully deleted!'
    login_url = 'login'


def fileDownloadView(self, slug):
    file_path = File.objects.get(slug=slug).source.path
    file_name = File.objects.get(slug=slug).name + File.objects.get(slug=slug).get_ext()

    myfile = open(file_path, 'rb')
    response = HttpResponse(myfile, content_type ='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response
