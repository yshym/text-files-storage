from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib.auth import get_user_model

import os, shutil
import textract, docx2txt

from slugify import slugify

from .validators import validate_file_extensions


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

    def __str__(self):
        return self.name

    def read_text_content(self):
        ext = os.path.splitext(self.source.path)[1]
        if ext == '.txt':
            with open(self.source.path) as f:
                return f.read()
        elif ext == '.docx':
            return docx2txt.process(self.source.path)
        elif ext == '.doc':
            return textract.process(self.source.path).decode('utf-8')
        elif ext == '.odt':
            return textract.process(self.source.path).decode('utf-8')

    def get_ext(self):
        ext = os.path.splitext(self.source.path)[1]
        return ext

    def remove_file(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.name))

    def delete(self, *args, **kwargs):
        self.remove_file()
        super(File, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(File, self).save(*args, **kwargs)
        self.text = self.read_text_content()
        super(File, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']


def pre_save_file_receiver(sender, instance, *args, **kwargs):
    if instance.name:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_file_receiver, sender=File)
