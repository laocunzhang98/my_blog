# Generated by Django 2.2.10 on 2020-04-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_yunicon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='icon',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='yunicon',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]