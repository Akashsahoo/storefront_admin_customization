from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

# Create your views here.
def say_hello(request):
    query_set = Product.objects.all()
    query_set = query_set.filter(collection__id=1)
    #query_set = query_set.filter(unit_price__gt=12)
    list(query_set)
    return render(request,'hello.html',{'name':'akash'})
