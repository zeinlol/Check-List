# Generated by Django 3.1.6 on 2021-02-18 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0005_auto_20210218_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='comments_images'),
        ),
    ]