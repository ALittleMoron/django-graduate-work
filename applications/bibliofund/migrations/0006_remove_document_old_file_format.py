# Generated by Django 3.2.9 on 2021-12-05 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliofund', '0005_auto_20211205_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='old_file_format',
        ),
    ]
