from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
                
    return int(round(distance, 3)*1000)

n_lojas = 0
lista_locs = []

#abrir e tratar arquivo
name = input("Digite o nome do arquivo: ")
file = open(name)
for line in file:
    #tirar os espaços em branco do arquivo
    line = line.rstrip()
    #caso seja a primeira linha do arquivo, ignorar e passar para a próxima
    if line.startswith("name"):
        continue
    else:
        local = line.split(',')
        n_lojas+=1
        #adiciona em lista_locs as latitudes e longitudes
        lista_locs.append([float(local[1]), float(local[2])])

matriz = []
#criar a matriz de distancias
for i in range(n_lojas):
    #para cada loja a visitar, criar uma linha na matriz
    linha_matriz = []
    #para cada elemento na linha, adicionar a distancia entre ele e os outros
    count = 0
    for j in range(n_lojas):
        linha_matriz.append(calculate_distance(lista_locs[i][0], lista_locs[i][1], lista_locs[j][0], lista_locs[j][1]))
    matriz.append(linha_matriz)
print(matriz)