# Generated by Django 2.0.1 on 2018-10-11 08:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_form', '0003_imagefile_projects_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=20)),
                ('file_name', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(default=datetime.datetime.now)),
                ('projects_name', models.CharField(max_length=20)),
                ('file', models.FileField(upload_to='files')),
            ],
            options={
                'verbose_name': 'ファイル',
                'verbose_name_plural': 'ファイル',
                'ordering': ['-upload_time'],
            },
        ),
    ]
