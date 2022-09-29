from django.shortcuts import render
from .models import campos

# Create your views here.

def muestraDatos(request):
    consulta = campos.objects.all()
    listaSuma = suma(consulta)
    contexto = zip(consulta, listaSuma)
    return render(request, 'blog/index.html', {'contexto': contexto})

def suma(lista):
    listaSuma = []
    for i in lista:
        listaSuma.append(i.var1 + i.var3 + i.var4)
    return listaSuma