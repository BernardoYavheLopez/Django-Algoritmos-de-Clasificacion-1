from django.shortcuts import render
from .models import campos
from django.http import HttpResponse
import math
from numpy import mean, var, exp
import numpy as np
import random
# Create your views here.

"""def muestraDatos(request):
    consulta = campos.objects.all()
    listaSuma = suma(consulta)
    contexto = zip(consulta, listaSuma)
    return render(request, 'blog/index.html', {'contexto': contexto})

def suma(lista):
    listaSuma = []
    for i in lista:
        listaSuma.append(i.var1 + i.var3 + i.var4)
    return listaSuma"""
def index(request):
    return render(request, 'blog/index.html', {})

def muestra_datos(request):
    consulta = campos.objects.all()
    LisSum = suma(consulta)
    contexto = zip(consulta, LisSum)
    return render(request, 'blog/post_list.html', {'contexto':contexto})

def suma(val):
    listSum = []
    for i in val:
        listSum.append(i.var1 + i.var3 + i.var4)
    return listSum

def algoritmo_knn(request):
    if request.method == 'GET':
        print('enviando datos')
        return render(request, 'blog/knn.html', {})
    else:
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        z = int(request.POST['z'])
        k = int(request.POST['k'])
        db = campos.objects.all()
        print(k,x,y,z)
        distancia = []
        for i in range(len(db)):
            val = math.sqrt(((x-db[i].var1)**2)+((y-db[i].var3)**2)+((z-db[i].var4)**2))
            distancia.append((db[i].var2, val))
        cont = { 'dist': distancia}
        #calculando distancia
        listK= distancia[:k]
        knn ={}
        letras=[]
        for i in listK:
            if i[0] in letras:
                knn[i[0]]+=1
            else:
                letras.append(i[0])
                knn[i[0]]=1
        cont['knn']=knn
    return render(request, 'blog/knn.html', cont)

###############################
def algoritmo_cbi(request):
    bd = list(campos.objects.all())
    new_bd = campos.objects.values('var2','var1','var3','var4').order_by('var2')
    letra=[]
    bd_final={}
    probabilidad=""
    cont=0
    for i in range(len(new_bd)):
        # si la letra no esta en el arreglo que haga esto, si no ignorar
        if bd[i].var2 in letra:
            cont+=1
        else:
            valor = campos.objects.filter(var2=bd[i].var2)
            letra.append(bd[i].var2)
            suma_num1=[]
            suma_num3=[]
            suma_num4=[]
            for j in list(valor):
                suma_num1.append(j.var1)
                suma_num3.append(j.var3)
                suma_num4.append(j.var4)
            media_num1=mean(suma_num1)
            varianza_num1= var(suma_num3)
            media_num3=mean(suma_num3)
            varianza_num3=var(suma_num3)
            media_num4=mean(suma_num4)
            varianza_num4=var(suma_num4)
            bd_final[bd[i].var2]=(media_num1,varianza_num1,media_num3,varianza_num3,media_num4,varianza_num4)
    para_evidencia = {}
    if request.method == 'POST':
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        z = int(request.POST['z'])
        p_letra = 1/len(bd_final)
        for l in range(len(bd_final)):
            para_evidencia[letra[l]]= pre_posteriori(bd_final[letra[l]][0],bd_final[letra[l]][2],bd_final[letra[l]][4],bd_final[letra[l]][1],bd_final[letra[l]][3],bd_final[letra[l]][5],x,y,z)

        evidcia = evidencia(para_evidencia,letra,p_letra)
        probabilidad = post_posteriori(para_evidencia,evidcia,letra)
        cont = {'letra': probabilidad}
    else:
        return render(request, 'blog/algoritmo_cbi.html', {})
    return render(request, 'blog/algoritmo_cbi.html', cont)


def pre_posteriori(media1,media3,media4,x1,x2,x3,x,y,z):
    var1 = random.randint(1, 10)
    var2 = random.randint(1, 10)
    var3 = random.randint(1, 10)
    p_num1 = (1/math.sqrt(2*math.pi*var1))* math.e*(pow(x-media1,2)/(2*x1))
    p_num3 = (1/math.sqrt(2*math.pi*var2))* math.e*(pow(y-media3,2)/(2*x2))
    p_num4 = (1/math.sqrt(2*math.pi*var3))* math.e*(pow(z-media4,2)/(2*x3))
    return (p_num1,p_num3,p_num4)

def post_posteriori(para_evidencia, evidencia,letras):
    rel = {}
    valores_rel =[]
    letra=""
    for i in range(len(para_evidencia)):
        val = (para_evidencia[letras[i]][0]*para_evidencia[letras[i]][1]*para_evidencia[letras[i]][2]) / evidencia
        rel[letras[i]]= val
        valores_rel.append(val)
    maximo = max(valores_rel) 
    keys = list(rel.keys())  
    for j in range(len(rel)):
        if rel[letras[j]] == maximo:
            letra = keys[j]
    return letra
def evidencia(para_evidencia,letras,p_letra):
    rel=[]
    for i in range(len(para_evidencia)):
        rel.append(p_letra*para_evidencia[letras[i]][0]*para_evidencia[letras[i]][1]*para_evidencia[letras[i]][2])
    resultado = sum(rel)
    return resultado

def calcular_varianza(arr, is_sample=False):
    media = (sum(arr) / len(arr))
    diff = [(v - media) for v in arr]
    sqr_diff = [d**2 for d in diff]
    sum__sqr_diff = sum(sqr_diff)

    if is_sample == True:
        variance = sum__sqr_diff/(len(arr)-1)
    else:
        variance = sum__sqr_diff/(len(arr)-1)
    return variance

#############################

def regresionLog(request):
    return render(request, 'blog/algoritmo_rl.html')

def interpretar(request):
    if request.GET["x1"].isdigit() and request.GET["x2"].isdigit():
        x1 = int(request.GET["x1"])
        x2 = int(request.GET["x2"])
        datos = campos.objects.all()
        b = calcConstante(datos)
        resultado  = valorReferente(datos, x1, x2, b)
        return render(request, 'blog/equivalente.html', {'consulta': resultado} )
    else:
        mensaje = "Te falto llenar o llenaste incorrectamente, recuerda que deben ser valores numericos"
    return HttpResponse(mensaje)

def valorReferente(datos, x1, x2, b):
    a1 = 0
    a2 = 0
    caracter = ''
    for i in datos:
        a1 = i.var1
        caracter = i.var2
        a2 = i.var3
        break
    salida = 1/(1 + np.exp(-(a1*x1 + a2*x2 + b)))
    if salida > 0.5:
        respuesta = f'El caracter obtenido es: {caracter}'
    else:
        respuesta = f'No hay caracter que haya podido encontrar: {caracter}'
    return respuesta

def calcConstante(datos):
    x = []
    y = []
    xCuadrada = 0
    xy = 0
    for i in datos:
        xCuadrada = xCuadrada + i.var1**2
        xy = xy + i.var1 * i.var3
        x.append(i.var1)
        y.append(i.var3)
    xSum = sum(x)
    ySum = sum(y)
    constante = (xCuadrada*ySum - xy*xSum)/(datos.count()*xCuadrada-xSum**2)
    return constante
    