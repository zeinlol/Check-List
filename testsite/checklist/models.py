import datetime

from django.conf import settings
from django.db import models


class Status(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class CheckList(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.TextField()
    done = models.BooleanField(default=False)
    date = models.DateField("Created", default=datetime.date.today)

    # users_with_access = models.ManyToManyField(User, related_name='store')     # Connect to user for access

    def __str__(self):
        return str(self.name)


# use one class for Categories/subtasks
class ListItem(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=150)
    done = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_index=True, null=True,
                               default=settings.DEFAULT_STATUS_ID)
    related_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, db_index=True, null=True,
                                     related_name='item_list')
    related_to = models.ForeignKey('self', on_delete=models.CASCADE, db_index=True, null=True, blank=True,
                                   related_name='related_items')
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments')
    date = models.DateField("Created", default=datetime.date.today)

    def __str__(self):
        return self.title


class Comment(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='comments_images', null=True, blank=True)
    file = models.FileField(upload_to='comments_files', null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name
