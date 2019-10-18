from django.db import models
from django.urls import reverse_lazy
from django.db.models.signals import pre_save, pre_delete, post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

import os, shutil, textract
import pypandoc

from slugify import slugify
from markdown_deux import markdown

from .validators import validate_file_extensions


class FileTag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def active(self):
        if File.objects.filter(tags=self):
            return True
        else:
            return False

    def num_of_inst(self):
        return File.objects.filter(tags=self).count()


def upload_location(instance, filename):
    ext = os.path.splitext(instance.source.path)[1]
    return f'{instance.name}/{instance.name + ext}'

class File(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    source = models.FileField(upload_to=upload_location,
                              validators = [validate_file_extensions])
    text = models.TextField()
    slug = models.SlugField(max_length=48)
    uploaded_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        FileTag,
        blank=True,
    )

    def __str__(self):
        return self.name

    def read_text_content(self):
        if self.get_ext() == '.txt':
            return pypandoc.convert_file(self.source.path, 'rst', format='rst')
        elif self.get_ext() == '.doc':
            return textract.process(self.source.path).decode('utf-8')
        else:
            return pypandoc.convert_file(self.source.path, 'rst', format=self.get_ext()[1:])

    def get_ext(self):
        ext = os.path.splitext(self.source.path)[1]
        return ext

    def get_markdown(self):
        content = self.text
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def remove_file(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.name))

    def save(self, *args, **kwargs):
        if not self.text:
            super(File, self).save(*args, **kwargs)
            self.text = self.read_text_content()
            super(File, self).save(*args, **kwargs)
        else:
            with open(self.source.path, 'w') as f:
                f.write(self.text)
            super(File, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse_lazy('file_detail', kwargs={'slug': str(self.slug)})


def pre_save_file_receiver(sender, instance, *args, **kwargs):
    if instance.name:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_file_receiver, sender=File)


def pre_delete_file_receiver(sender, instance, *args, **kwargs):
    instance.remove_file()

pre_delete.connect(pre_delete_file_receiver, sender=File)


def post_save_file_receiver(sender, instance, *args, **kwargs):
    for f in os.listdir(settings.MEDIA_ROOT):
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, f)):
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

post_save.connect(post_save_file_receiver, sender=File)
