# Generated by Django 3.1.6 on 2021-02-19 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0006_comment_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subcategories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.category'),
        ),
    ]
