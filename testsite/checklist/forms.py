from django import forms
from .models import CheckList, Comment, Category, SubTask#,Image


class ListForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ["name",  "description", "completed", "date"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'photo')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)



class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ('title', )


# for multiple photos
# class CommentImagesForm(forms.Form):
#
#     photos = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
#
#
#     def __init__(self, *args, **kwargs):
#         if 'request' in kwargs:
#             self.request = kwargs.pop('request')
#         super().__init__(*args, **kwargs)
#
#     def save_for(self, comment):
#         for photo in self.cleaned_data['photos']:
#             Image(photo=photo, comment=comment).save()
