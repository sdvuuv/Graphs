import graph
import antcolony
import filereading

#g = filereading.read_file('1000.txt')
# Задаем класс с муравьями 
g = graph.Graph(6)

# 1 с 2, 5
g.add_edge(0, 1, 3)
g.add_edge(0, 4, 1)
# 2 c 1, 6, 3
g.add_edge(1, 0, 3)
g.add_edge(1, 5, 3)
g.add_edge(1, 2, 8)
# 3 c 2, 6, 4
g.add_edge(2, 1, 3)
g.add_edge(2, 5, 1)
g.add_edge(2, 3, 1)
# 4 c 3, 5
g.add_edge(3, 2, 8)
g.add_edge(3, 4, 1)
# 5 c 1, 4
g.add_edge(4, 0, 3)
g.add_edge(4, 3, 3)
# 6 c 1, 2, 3, 4, 5
g.add_edge(5, 0, 3)
g.add_edge(5, 1, 3)
g.add_edge(5, 2, 3)
g.add_edge(5, 3, 5)
g.add_edge(5, 4, 4)

colony = antcolony.AntColony(g, n_iterations=100, n_ants=10, alpha=1, beta=2, evaporation_rate=0.5)
best_path, best_path_length, all_paths = colony.run(start_vertex=0)



print("Лучший путь:", best_path)
print("Длина пути:", best_path_length)

print("Все пути:", all_paths)


