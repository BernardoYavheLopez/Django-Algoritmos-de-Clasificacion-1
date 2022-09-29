import random
import string 

columna1 = []
columna2 = []
columna3 = []
columna4 = []

ingresa = int(input("Ingrese la cantidad de lineas: "))
for i in range(ingresa):
    columna1.append(random.randint(0,5000))
    columna2.append(random.choice(string.ascii_letters))
    columna3.append(random.randint(0,5000))
    columna4.append(random.randint(0,5000))
    
f = open("paraPoblar.csv",'w')
for i in range(len(columna1)):
    titulo="Columna1 \tColumna2 \tColumna3 \tColumna4 "
    f.write('{},{},{},{}\n'.format(columna1[i], columna2[i], columna3[i], columna4[i]))
f.close()