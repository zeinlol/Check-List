from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import CheckList, Category, SubTask, Comment, Image
from .forms import ListForm, CommentForm, CommentImagesForm
from django.views import View
from django.contrib import messages
from django.urls import reverse


def show_lists(request):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(request.META.get('HTTP_REFERER'))
    else:
        checklists = CheckList.objects.all().order_by("-date")[:20]
        return render(request, 'checklist/checklist_list.html', {'checklists': checklists})


# Bullshit
def cross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect(r'/')


def uncross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect(r'/')


def cross_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.completed = True
    item.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.completed = False
    item.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cross_subtask(request, item_id):
    item = SubTask.objects.get(pk=item_id)
    item.completed = True
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_subtask(request, item_id):
    item = SubTask.objects.get(pk=item_id)
    item.completed = False
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CreateImageView(View):
    form_images_class = CommentImagesForm
    model = Comment

    def get(self, request):
        form_images = self.form_images_class()
        return form_images

    def post(self, request):
        form = request.POST
        form_images = self.form_images_class(request.POST, request.FILES, request=request)
        if form_images.is_valid():
            image = form.save()
            form_images.save_for(image)
            return HttpResponseRedirect('/')

        return HttpResponseRedirect('/')


def show_full_list(request, list_id):
    checklist = CheckList.objects.get(pk=list_id)
    # categories = Category.objects.filter(related_list_id=checklist).order_by('id')
    categories = checklist.categories.order_by('id')
    subtasks = list()
    for each in categories:
        subtasks.append(list(SubTask.objects.filter(related_category_id=each).order_by('id')))
    # subtasks = SubTask.objects.filter(related_category=categories).order_by('id')

    comments = checklist.comments.filter(active=True)
    images = Image.objects.filter()[:5]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        form_images = CommentImagesForm(request.POST, request.FILES, request=request)
        if comment_form.is_valid() and form_images.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = checklist
            # Save the comment to the database
            form_images.save_for(new_comment.save())
            new_comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        comment_form = CommentForm()
        form_images = CommentImagesForm()
    return render(request, 'checklist/list_view.html',
                           {'checklist': checklist, 'categories': categories, 'subtasks': subtasks,
                            'comments': comments,
                            'comment_form': comment_form,
                            'images': images,
                            'form_images': form_images})
