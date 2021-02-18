from django import forms
from .models import CheckList, Comment, Category, SubTask, Image


class ListForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ["name",  "description", "completed", "date"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class CategoryForm(forms.ModelForm):
    model = Category
    fields = ('title', 'completed', 'related_list')


class SubTaskForm(forms.ModelForm):
    model = SubTask
    fields = ('title', 'completed', 'related_category')


class CommentImagesForm(forms.Form):

    photos = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))


    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save_for(self, advert):
        for photo in self.cleaned_data['photos']:
            Image(photo=photo, advert=advert).save()
