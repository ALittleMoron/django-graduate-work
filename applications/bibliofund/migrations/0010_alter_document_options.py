# Generated by Django 4.0.2 on 2022-02-27 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliofund', '0009_remove_filestatistic_dislike_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Документ', 'verbose_name_plural': 'Документы'},
        ),
    ]
