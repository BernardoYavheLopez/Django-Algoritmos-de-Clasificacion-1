from django.shortcuts import render
from .models import Blog

def muestra_datos(request):
    consulta = Blog.objects.all()
    SumaList = suma(consulta)
    contexto = zip(consulta, SumaList)
    return render(request, 'blog/post_list.html',{'contexto':contexto})

# Create your views here.
def suma(val):
    SumaList = []
    for i in val:
        SumaList.append(i.x1 + i.x3 + i.x4)
    return SumaList
