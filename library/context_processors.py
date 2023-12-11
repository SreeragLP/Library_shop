from library.models import Category

def menu_links(request):
    mybooks=Category.objects.all()
    return {'mybooks':mybooks}