# Generated by Django 2.1.5 on 2019-02-01 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
