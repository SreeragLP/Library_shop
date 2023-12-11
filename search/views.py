from django.shortcuts import render
from library.models import Books
from django.db.models import Q


# Create your views here.
def searchresult(request):
    query = ""
    books=None
    if (request.method=="POST"):
        query=request.POST['q']
        if query:
            books=Books.objects.filter(Q(bname__icontains=query) | Q(description__icontains=query))

    return render(request,'search/search.html',{'b':books,'q':query})

