from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CheckList
from .forms import ListForm
from django.contrib import messages


def show_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():
            form.save()
            checklists = CheckList.objects.all().order_by("-date")[:20]
            messages.success(request, 'Item added!')
            return render(request, 'checklist/checklist_list.html', {'checklists': checklists})
    else:
        checklists = CheckList.objects.all().order_by("-date")[:20]
        return render(request, 'checklist/checklist_list.html', {'checklists': checklists})

    # checklists = CheckList.objects.all().order_by("-date")[:20]
    # return render(request, 'checklist/checklist_list.html', {'checklists': checklists})


def cross_item(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect(r'/')


def uncross_item(request, list_id):
    item = CheckList.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect(r'/')

