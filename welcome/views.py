from django.shortcuts import render

def index(request) :
    return render(request, 'welcome/index.html')


# Create your views here.
