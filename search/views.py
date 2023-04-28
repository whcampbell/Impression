from django.shortcuts import render
from django.views.generic import ListView
from users.models import CustomUser

class SearchResultView(ListView) :
    model = CustomUser
    template_name = 'search/results.html'

def search(request) :
    return render(request, 'search/search.html')

# Create your views here.
