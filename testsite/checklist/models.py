from django.db import models
import datetime


class CheckList(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    date = models.DateField("Created", default=datetime.date.today)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    related_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, db_index=True, null=True, related_name='categories')

    def __str__(self):
        return self.title


class SubTask(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    related_category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True, null=True, related_name='subtasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class Image(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='image')
    photo = models.ImageField(upload_to='comments_images')
