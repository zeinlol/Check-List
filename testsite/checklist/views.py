from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import ListForm, CommentForm, ItemForm
from .models import CheckList, ListItem, Status
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, CheckListSerializer, ListItemSerializer


class CheckListViewSet(viewsets.ModelViewSet):
    queryset = CheckList.objects.all().order_by('-date')
    serializer_class = CheckListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# # # # # # # # # # # # # # #  OLD FUNCTIONS
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
# Bullshit  (OLD BLOCK)
def cross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = True
    item.save()
    categories = item.item_list.order_by('id')
    for task in categories:
        cross_item(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_list(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = False
    item.save()
    categories = item.item_list.order_by('id')
    for task in categories:
        uncross_item(request, task.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cross_item(request, item_id):
    item = ListItem.objects.get(pk=item_id)
    item.completed = True
    item.status = Status.objects.get(pk=settings.CROSSED_STATUS_ID)
    item.save()
    sub_item = item.related_items.order_by('id')
    for task in sub_item:
        cross_item(request, task.id)

    all_items_completed = True
    try:
        category = ListItem.objects.get(related_items=item)
        subtasks = category.related_items.order_by('id')
        for task in subtasks:
            if task.completed is False:
                all_items_completed = False
        if all_items_completed:
            category.completed = True
            category.status = Status.objects.get(pk=settings.CROSSED_STATUS_ID)
            category.save()
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def uncross_item(request, item_id):
    item = ListItem.objects.get(pk=item_id)
    item.completed = False
    item.status = Status.objects.get(pk=settings.UNCROSSED_STATUS_ID)
    item.save()
    sub_item = item.related_items.order_by('id')
    for task in sub_item:
        uncross_item(request, task.id)
    try:
        category = ListItem.objects.get(related_items=item)
        category.completed = False
        category.save()
    except:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_item(item_id):
    item = ListItem.objects.get(pk=item_id)
    sub_item = item.related_items.order_by('id')
    for task in sub_item:
        delete_item(task.id)
    item.delete()
    return


def delete_list(list_id):
    checklist = CheckList.objects.get(pk=list_id)
    items = ListItem.objects.filter(related_list=checklist)
    for task in items:
        delete_item(task.id)
    checklist.delete()
    return


def show_full_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    category_items = checklist.item_list.order_by('id')
    statuses = Status.objects.filter().order_by('id')
    subtask_items = []
    for each in category_items:
        subtask_items.append(each.related_items.order_by('id'))
    list_items = zip(category_items, subtask_items)

    if request.method == 'POST' and 'change_status' in request.POST:
        item = get_object_or_404(ListItem, pk=request.POST.get('item_id'))
        status = get_object_or_404(Status, pk=request.POST.get('status_id'))
        item.status = status
        item.save()
        if status.id == 2:
            cross_item(request, item.id)
        else:
            uncross_item(request, item.id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
            task_id = request.POST.get('item_id')
            new_comment.comments.set(ListItem.objects.filter(pk=task_id))
            new_comment.save()
            new_comment.photo = request.FILES.get('photo')
            new_comment.file = request.FILES.get('file')
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        comment_form = CommentForm()
    return render(request, 'checklist/list_view.html',
                  {'checklist': checklist,
                   'statuses': statuses,
                   'list_items': list_items,
                   'comment_form': comment_form})


def edit_list(request, list_id):
    checklist = get_object_or_404(CheckList, pk=list_id)
    category_items = checklist.item_list.order_by('id')
    subtasks_item = []
    for each in category_items:
        subtasks_item.append(each.related_items.order_by('id'))
    new_list_items = zip(category_items, subtasks_item)

    if request.method == 'POST' and 'new_name' in request.POST:
        item = get_object_or_404(ListItem, pk=request.POST.get('item_id'))
        item.title = request.POST.get('new_name')
        item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
            new_cat.related_to = get_object_or_404(ListItem, pk=request.POST.get('item_id'))
            new_cat.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'delete_item' in request.POST:
        delete_item(request.POST.get('item_id'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST' and 'delete_list' in request.POST:
        delete_list(request.POST.get('list_id'))

        return HttpResponseRedirect('/')

    else:
        item_form = ItemForm
    return render(request, 'checklist/edit_list.html',
                  {
                      'new_list_items': new_list_items,
                      'item_form': item_form,
                      'checklist': checklist})
