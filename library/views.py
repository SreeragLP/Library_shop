from django.shortcuts import render,redirect
from library.models import Category,Books
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    c = Category.objects.all()
    return render(request, 'library/home.html', {'c': c})


def books(request,c):
    b = Books.objects.filter(category__cname=c)
    category = Category.objects.get(cname=c)

    return render(request,'library/books.html',{'b':b,'category':category})


def detailed_view(request,p):
    d = Books.objects.get(bname=p)
    return render(request,'library/detailed_view.html',{'d':d})



def register(request):
    if(request.method=="POST"):
        u = request.POST['u']
        p = request.POST['p']
        p1 = request.POST['p1']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        if(p==p1):
            u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            u.save()
            return redirect('library:home')

    return render(request,'library/register.html')


def user_login(request):
    if (request.method == "POST"):
        u = (request.POST['u'])
        p = (request.POST['p'])
        user = authenticate(username=u, password=p)

        if user:
            login(request,user)
            return redirect('library:home')
        else:
            messages.error(request, "invalid credentails")
    return render(request,'library/login.html')



def user_logout(request):
    logout(request)
    return user_login(request)






