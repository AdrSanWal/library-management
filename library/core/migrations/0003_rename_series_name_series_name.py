# Generated by Django 3.2 on 2021-12-20 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_book_series'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='series_name',
            new_name='name',
        ),
    ]
