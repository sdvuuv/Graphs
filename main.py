from queue import PriorityQueue
import graph

def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D
 



g = graph.Graph(9)

# 1 с 2, 4, 3
g.add_edge(0, 1, 10)
g.add_edge(0, 3, 8)
g.add_edge(0, 2, 6)
# 2 c 4, 7, 5
g.add_edge(1, 6, 11)
g.add_edge(1, 3, 5)
g.add_edge(1, 4, 13)
# 3 c 5
g.add_edge(2, 4, 3)
# 4 c 6, 7, 5
g.add_edge(3, 6, 12)
g.add_edge(3, 5, 7)
g.add_edge(3, 4, 5)
# 5 c 6, 9
g.add_edge(4, 5, 9)
g.add_edge(4, 8, 12)
# 6 c 8, 9
g.add_edge(5, 7, 8)
g.add_edge(5, 8, 10)
# 7 c 6, 8, 9
g.add_edge(6, 5, 4)
g.add_edge(6, 7, 6)
g.add_edge(6, 8, 16)
# 8 c 9
g.add_edge(7, 8, 15)


D = dijkstra(g, 0)
print("Самый короткий путь:", D[8])




