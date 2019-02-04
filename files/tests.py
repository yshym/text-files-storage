from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os, shutil

from .models import File


class FileListPageTests(TestCase):

    def test_file_list_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_list.html')


class FileDetailPageTests(TestCase):

    def create_file(self):
        testfile = open(os.path.join(settings.BASE_DIR, 'test.txt'), 'rb')
        self.testfile, created = File.objects.get_or_create(
            name='testname',
            source= SimpleUploadedFile('test.txt', testfile.read()),
            description='testdescription'
        )

    def remove_file(self):
        if self.testfile:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.testfile.name))

    def test_file_detail_page_status_code_200(self):
        self.create_file()
        response = self.client.get(
            reverse(
                'file_detail',
                kwargs={'slug': self.testfile.slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.remove_file()

    def test_file_detail_page_status_code_404(self):
        self.create_file()
        response = self.client.get(
            reverse(
                'file_detail',
                kwargs={'slug': self.testfile.slug+self.testfile.slug}
            )
        )
        self.assertEqual(response.status_code, 404)
        self.remove_file()

    def test_view_uses_correct_template(self):
        self.create_file()
        response = self.client.get(reverse('file_detail', kwargs={'slug': self.testfile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_detail.html')
        self.remove_file()

