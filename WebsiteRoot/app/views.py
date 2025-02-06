from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the index page of the application, i.e the first page that any user will see")
