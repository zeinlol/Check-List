from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import CheckList, Category, SubTask, ListItem, Status
from .forms import ListForm, CommentForm, CategoryForm, SubTaskForm, ItemForm
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
        return render(request, 'checklist/checklist_list.html', {'checklists': checklists,
                                                                 'add_list_form': add_list_form})


# # # # # # # # # # # # #  NEW CROSS/UNCROSS BLOCK
def cross_item(request, item_id):
    item = ListItem.objects.get(pk=item_id)
    item.completed = True
    item.status = Status.objects.get(Title='Done')
    item.save()
    sub_item = item.related_items.order_by('id')
    for task in sub_item:
        cross_item(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_item(item_id):
    item = ListItem.objects.get(pk=item_id)
    sub_item = item.related_items.order_by('id')
    for task in sub_item:
        delete_item(task.id)
    item.delete()
    return


# Bullshit  (OLD BLOCK)
def cross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = True
    item.save()
    categories = item.categories.order_by('id')
    for task in categories:
        cross_category(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = False
    item.save()
    categories = item.categories.order_by('id')
    for task in categories:
        uncross_category(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cross_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.completed = True
    item.status = Status.objects.get(Title='Done')
    item.save()
    subtasks = item.subtasks.order_by('id')
    for task in subtasks:
        cross_subtask(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_category(request, category_id):
    item = Category.objects.get(pk=category_id)
    item.completed = False
    item.status = Status.objects.get(title='Untouched')
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


#    OLD LIST VIEW
# def show_full_list(request, list_id):
#     checklist = get_object_or_404(CheckList, pk=list_id)
#     categories = checklist.categories.order_by('id')
#     subtasks = []
#     for each in categories:
#         subtasks.append(SubTask.objects.filter(related_category_id=each).order_by('id'))
#     list_items = zip(categories, subtasks)
#
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.save()
#             task_id = request.POST.get('subtask_id')
#             new_comment.post.set(SubTask.objects.filter(pk=task_id))
#             new_comment.save()
#             new_comment.photo = request.FILES.get('photo')
#             new_comment.file = request.FILES.get('file')
#             new_comment.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#     else:
#         print(request.POST)
#         comment_form = CommentForm()
#     return render(request, 'checklist/list_view.html',
#                            {'checklist': checklist, 'categories': categories,
#                             'list_items': list_items,
#                             'comment_form': comment_form})


def show_full_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    categories = checklist.categories.order_by('id')
    category_items = checklist.item_list.order_by('id')
    print(category_items)
    subtasks = []
    for each in categories:
        subtasks.append(SubTask.objects.filter(related_category_id=each).order_by('id'))
    list_items = zip(categories, subtasks)
    subtask_items = []
    for each in category_items:
        subtask_items.append(ListItem.objects.filter(related_items=each).order_by('id'))
    new_list_items = zip(category_items, subtask_items)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
            task_id = request.POST.get('subtask_id')
            new_comment.post.set(SubTask.objects.filter(pk=task_id))
            new_comment.save()
            new_comment.photo = request.FILES.get('photo')
            new_comment.file = request.FILES.get('file')
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print(request.POST)
        comment_form = CommentForm()
    return render(request, 'checklist/list_view.html',
                  {'checklist': checklist, 'categories': categories,
                   'list_items': list_items,
                   'list_new_items': new_list_items,
                   'comment_form': comment_form})


def edit_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    categories = checklist.categories.order_by('id')
    category_items = checklist.item_list.order_by('id')
    subtasks = []
    for each in categories:
        subtasks.append(SubTask.objects.filter(related_category_id=each).order_by('id'))
    subtasks_item = []
    for each in category_items:
        subtasks_item.append(ListItem.objects.filter(related_items=each).order_by('id'))
    list_items = zip(categories, subtasks)
    new_list_items = zip(category_items, subtasks_item)

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

    # # # # # # # # # # # # # NEW ITEM FORM
    if request.method == 'POST' and 'new_category' in request.POST:
        form = ItemForm(request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.related_list = checklist
            new_cat.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'new_item' in request.POST:
        form = ItemForm(request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.related_item = request.POST.get('item_id')
            new_cat.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'delete_item' in request.POST:
        delete_item(request.POST.get('item_id'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    else:
        categories_form = CategoryForm
        subtask_form = SubTaskForm
        item_form = ItemForm
    return render(request, 'checklist/edit_list.html',
                  {'list_items': list_items,
                   'new_list_items': new_list_items,
                   'categories_form': categories_form,
                   'item_form': item_form,
                   'category_items': category_items,
                   'checklist': checklist,
                   'subtask_form': subtask_form})
