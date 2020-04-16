from django.shortcuts import render,redirect
from .models import Item
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home_page(request):
    return render(request,'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request,'list.html',{'items': items})

@csrf_exempt
def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')