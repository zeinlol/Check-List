from django import forms
from .models import CheckList, Comment, Category, SubTask, ListItem


class ListForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ["name",  "description", "completed", "date"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'photo', 'file')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ('title',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ('title', )
