from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from math import *

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

def create_data_model():
    """armazena os dados para o problema"""
    data = {}
    data['distance_matrix'] = matriz
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def print_solution(manager, routing, solution):
    """mostra a solução no console."""
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}Km\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()