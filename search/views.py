from django.shortcuts import render
from django.db.models import Q
from users.models import CustomUser
from .forms import SearchForm

# I split this into a different app before I knew that apps need not be split up,
# in fact it just makes imports more hairy. but hey here we are
def search(request) :
    if (not request.GET) :
        form = SearchForm()
        return render(request, 'search/search.html', {'form':form})
    form = SearchForm(request.GET)
    query = request.GET.get("search_query")
    results = CustomUser.objects.filter(Q(username__icontains=query) | Q(description__icontains=query))
    context = {
        'form':form,
        'results':results,
    }
    return render(request, 'search/search.html', context)

# Create your views here.
