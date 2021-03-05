# Generated by Django 3.1.6 on 2021-03-05 09:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('completed', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='comments_images')),
                ('file', models.FileField(blank=True, null=True, upload_to='comments_files')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('completed', models.BooleanField(default=False)),
                ('comments', models.ManyToManyField(blank=True, related_name='post', to='checklist.Comment')),
                ('related_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='checklist.category')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.status')),
            ],
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('completed', models.BooleanField(default=False)),
                ('comments', models.ManyToManyField(blank=True, related_name='comments', to='checklist.Comment')),
                ('related_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_list', to='checklist.checklist')),
                ('related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_items', to='checklist.listitem')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.status')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='related_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='checklist.checklist'),
        ),
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.status'),
        ),
    ]
