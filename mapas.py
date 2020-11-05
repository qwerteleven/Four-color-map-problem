from minizinc import Instance, Model, Solver
import csv
from IPython.display import FileLink
import os
import datetime

delta = datetime.timedelta(minutes=10)


for dirname, _, filenames in os.walk('./data'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


def submission_generation(filename, str_output):
    os.chdir(r'./result')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in str_output:
            writer.writerow(item)
    return FileLink(filename)


def solver(map,nodos,aristas,model):
    mapas = Model(model)
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, mapas)
    instance["aristas_count"] = aristas
    instance["map"] = map
    instance["node_count"] = nodos
    result = instance.solve(timeout=delta)
    # Output the array q
    return result["colores"]



def check_solution(node_count, edges, solution):
    for edge in edges:
        if solution[edge[0]] == solution[edge[1]]:
            print("solución inválida, dos nodos adyacentes tienen el mismo color")
            return 0
    value = max(solution) + 1  # add one because minimum color is 0

    return value


def realSolution(array):
    aux = min(array)
    for i in range(len(array)):
        array[i] = array[i] - aux
    return array


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    mapa = []
    mapaset = []
    solution = range(0, node_count)

    for i in range(node_count):
        mapa.append([])

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

        mapa[int(parts[0])].append(int(parts[1]) + 1)
        mapa[int(parts[1])].append(int(parts[0]) + 1)

    for i in range(len(mapa)):
        mapaset.append(set(mapa[i]))

    solution = solver(mapaset, node_count, edge_count, "./mapas1.mzn")
    solution = realSolution(solution)

    solutiona = solver(mapaset, node_count, edge_count, "./mapas.mzn")
    solutiona = realSolution(solutiona)

    if max(solutiona) < max(solution):
        solution = solutiona

    file = open("gc_solution_" + str(node_count) + "_" + str(edge_count) +".txt", "w")
    file.write(str(solution) + str([max(solution) + 1]))
    file.close()


    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data, check_solution(node_count, edges, solution)


str_output = [["Filename","Min_value"]]

for dirname, _, filenames in os.walk('./data'):
    for filename in filenames:
        full_name = dirname+'/'+filename
        with open(full_name, 'r') as input_data_file:
            input_data = input_data_file.read()
            output, value = solve_it(input_data)
            str_output.append([filename,str(value)])

submission_generation('sample.csv', str_output)