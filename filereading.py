import graph
def read_file(name_of_file, ):
    with open(name_of_file, "r") as file:
        line_count = sum(1 for line in file) - 1 
        g = graph.Graph(line_count)
        for line in file:
            arr = line.split()
            g.add_edge(int(arr[0]), int(arr[1]), int(arr[2]))

        return g


