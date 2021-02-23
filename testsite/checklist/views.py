from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import CheckList, Category, SubTask, Comment# , Image
from .forms import ListForm, CommentForm, CategoryForm, SubTaskForm# , CommentImagesForm
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404


def show_lists(request):
    add_list_form = ListForm
    checklists = CheckList.objects.all().order_by("-date")[:20]
    if request.method == 'POST' and 'delete_list' in request.POST:
        delete_list(request.POST.get('list_id'))

        return render(request, 'checklist/checklist_list.html',
                      {'checklists': checklists, 'add_list_form': add_list_form})
    elif request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseRedirect('/')

    else:
        return render(request, 'checklist/checklist_list.html', {'checklists': checklists, 'add_list_form': add_list_form})


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
    subtasks = item.subtasks.order_by('id')
    for task in subtasks:
        cross_subtask(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.completed = False
    item.save()
    subtasks = item.subtasks.order_by('id')
    for task in subtasks:
        uncross_subtasks(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cross_subtask(request, item_id):
    item = SubTask.objects.get(pk=item_id)
    item.completed = True
    item.save()
    all_st_completed = True
    category = Category.objects.get(subtasks=item)
    subtasks = category.subtasks.order_by('id')
    for task in subtasks:
        if task.completed is False:
            all_st_completed = False
    if all_st_completed:
        category.completed = True
        category.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_subtasks(request, item_id):
    item = SubTask.objects.get(pk=item_id)
    item.completed = False
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_subtask(request, item_id):
    item = SubTask.objects.get(pk=item_id)
    item.completed = False
    item.save()
    category = Category.objects.filter(subtasks=item)
    for each in category:
        each = Category.objects.get(pk=each.id)
        each.completed = False
        each.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_subtask(categy_id):
    subtask = SubTask.objects.get(pk=categy_id)
    subtask.delete()
    return


def delete_category(category_id):
    category = Category.objects.get(pk=category_id)
    subtasks = SubTask.objects.filter(related_category=category)
    for task in subtasks:
        delete_subtask(task.id)
    category.delete()
    return


def delete_list(list_id):
    checklist = CheckList.objects.get(pk=list_id)
    categories = Category.objects.filter(related_list=checklist)
    for task in categories:
        delete_category(task.id)
    checklist.delete()
    return

# class CreateImageView(View):
#     form_images_class = CommentImagesForm
#     model = Comment
#
#     def get(self, request):
#         form_images = self.form_images_class()
#         return form_images
#
#     def post(self, request):
#         form = request.POST
#         form_images = self.form_images_class(request.POST, request.FILES, request=request)
#         if form_images.is_valid():
#             image = form.save()
#             form_images.save_for(image)
#             return HttpResponseRedirect('/')
#
#         return HttpResponseRedirect('/')


def show_full_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    categories = checklist.categories.order_by('id')
    subtasks = []
    comments = []
    for each in categories:
        subtasks.append(SubTask.objects.filter(related_category_id=each).order_by('id'))
    #for each in subtasks:
    #    comments.append(SubTask.objects.get(id=each.id).comments.order_by('id'))
    #print(comments)
    list_items = zip(categories, subtasks)
    #comments_list = zip(subtasks, comments)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
            task_id = request.POST.get('subtask_id')
            new_comment.post.set(SubTask.objects.filter(pk=task_id))
            new_comment.save()
            new_comment.photo = request.FILES.get('photo')
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print(request.POST)
        comment_form = CommentForm()
    return render(request, 'checklist/list_view.html',
                           {'checklist': checklist, 'categories': categories, 'subtasks': subtasks,
                            'list_items': list_items,
                            #'comments_list': comments_list,
                            'comment_form': comment_form})


def edit_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    categories = checklist.categories.order_by('id')
    subtasks = []
    for each in categories:
        subtasks.append(SubTask.objects.filter(related_category_id=each).order_by('id'))
    list_items = zip(categories, subtasks)

    if request.method == 'POST' and 'category' in request.POST:
        categories_form = CategoryForm(request.POST)
        if categories_form.is_valid():
            new_cat = categories_form.save(commit=False)
            new_cat.related_list = checklist
            new_cat.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'subtask' in request.POST:
        subtask_form = SubTaskForm(request.POST)
        if subtask_form.is_valid():
            new_task = subtask_form.save(commit=False)
            new_task.related_category = Category.objects.get(pk=int(request.POST.get('category_id')))
            new_task.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'delete_list' in request.POST:
        delete_list(request.POST.get('list_id'))

        return HttpResponseRedirect('/')

    if request.method == 'POST' and 'delete_category' in request.POST:
        delete_category(request.POST.get('category_id'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'delete_subtask' in request.POST:
        delete_subtask(request.POST.get('subtask_id'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        categories_form = CategoryForm
        subtask_form = SubTaskForm
    return render(request, 'checklist/edit_list.html',
                           {'list_items': list_items,
                            'categories_form': categories_form,
                            'checklist': checklist,
                            'subtask_form': subtask_form})
