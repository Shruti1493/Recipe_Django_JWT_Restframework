# Generated by Django 4.2.6 on 2023-11-07 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_blog_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='Recipe',
        ),
    ]