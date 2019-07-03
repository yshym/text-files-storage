# Generated by Django 2.1.7 on 2019-02-15 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_auto_20190215_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='tags',
        ),
        migrations.AddField(
            model_name='file',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='files.FileTag'),
        ),
    ]