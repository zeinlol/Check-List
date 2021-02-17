from django.db import models
import datetime


class CheckList(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    date = models.DateField("Created", default=datetime.date.today)

    def __str__(self):
        return str(self.name) + ' | ' + str(self.completed)


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
