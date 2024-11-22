import random
import graph

class AntColony:
    def __init__(self, graph, n_ants, n_iterations, alpha, beta, evaporation_rate, q=1):
        self.graph = graph  # Граф на основе вашего класса
        self.n_ants = n_ants  # Количество муравьев
        self.n_iterations = n_iterations  # Количество итераций
        self.alpha = alpha  # Влияние феромона
        self.beta = beta  # Коэфицент влияния весов или феромонов на выбор обхода
        self.evaporation_rate = evaporation_rate  # Коэффициент испарения
        self.q = q  # Константа для обновления феромона
        self.pheromones = [[1 for _ in range(graph.v)] for _ in range(graph.v)]  # Изначально одинаковый уровень феромона

    def run(self, start_vertex):
        """
        Запуск муравьиного алгоритма.

        :param start_vertex: Стартовая вершина для всех муравьев
        :return: Кратчайший путь и его длина
        """
        best_path = None
        best_path_length = float('inf') # Начальное значение — бесконечность

        for iteration in range(self.n_iterations):
            all_paths = []  # Список всех путей
            all_path_lengths = []  # Длины всех путей
            # Каждый муравей строит свой путь
            for ant in range(self.n_ants):
                path, path_length = self.construct_solution(start_vertex)
                all_paths.append(path)
                all_path_lengths.append(path_length)
                # Обновляем лучший маршрут
                if path_length < best_path_length:
                    best_path_length = path_length
                    best_path = path
            # Обновляем феромоны на основе найденных маршрутов
            self.update_pheromones(all_paths, all_path_lengths)

        return best_path, best_path_length

    def construct_solution(self, start_vertex):
        """
        Построение маршрута одним муравьем.

        :param start_vertex: Стартовая вершина
        :return: Построенный маршрут и его длина
        """
        path = [start_vertex]  # Начинаем с заданной стартовой вершины
        path_length = 0  # Изначальная длина пути равна 0
        current_vertex = start_vertex

        # Строим маршрут, пока не будут пройдены все вершины
        while len(path) < self.graph.v:
            probabilities = self.calculate_transition_probabilities(current_vertex, path)  # Вероятности перехода
            next_vertex = self.select_next_vertex(probabilities)  # Выбираем следующую вершину
            path.append(next_vertex)  # Добавляем её в маршрут
            path_length += self.graph.edges[current_vertex][next_vertex]  # Увеличиваем длину пути
            current_vertex = next_vertex  # Переходим в следующую вершину

        # Возвращаемся к стартовой вершине, чтобы завершить цикл
        path_length += self.graph.edges[current_vertex][start_vertex]
        path.append(start_vertex)

        return path, path_length

    def calculate_transition_probabilities(self, current_vertex, visited):
        """
        Вычисление вероятностей перехода в соседние вершины.

        :param current_vertex: Текущая вершина
        :param visited: Список уже посещённых вершин
        :return: Список вероятностей перехода для каждой вершины
        """
        probabilities = [0] * self.graph.v  # Изначально вероятности равны 0
        total = 0  # Сумма значений для нормализации

        # Рассчитываем вероятность перехода в каждую из соседних вершин
        for neighbor in range(self.graph.v):
            if neighbor not in visited and self.graph.edges[current_vertex][neighbor] > 0:
                # Учитываем феромон и эвристику (обратное расстояние)
                pheromone = self.pheromones[current_vertex][neighbor] ** self.alpha
                distance = (1 / self.graph.edges[current_vertex][neighbor]) ** self.beta
                probabilities[neighbor] = pheromone * distance
                total += probabilities[neighbor]

        # Нормализация вероятностей (чтобы сумма равнялась 1)
        if total > 0:
            probabilities = [p / total for p in probabilities]

        return probabilities

    def select_next_vertex(self, probabilities):
        """
        Выбор следующей вершины на основе вероятностей.

        :param probabilities: Вероятности перехода в соседние вершины
        :return: Выбранная вершина
        """
        r = random.random()  # Случайное число от 0 до 1
        cumulative = 0  # Накопленная сумма вероятностей

        # Сравниваем случайное число с накопленной суммой вероятностей
        for vertex, probability in enumerate(probabilities):
            cumulative += probability
            if r <= cumulative:
                return vertex

        # Если случайное число не соответствует ни одной вершине, выбираем вершину с макс. вероятностью
        return probabilities.index(max(probabilities))

    def update_pheromones(self, paths, path_lengths):
        """
        Обновление уровня феромонов на рёбрах графа.

        :param paths: Список маршрутов всех муравьев
        :param path_lengths: Список длин соответствующих маршрутов
        """
        # Испарение феромона на всех рёбрах
        for i in range(self.graph.v):
            for j in range(self.graph.v):
                self.pheromones[i][j] *= (1 - self.evaporation_rate)

        # Добавление нового феромона на основе найденных маршрутов
        for path, length in zip(paths, path_lengths):
            pheromone_contribution = self.q / length  # Количество феромона зависит от длины пути

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.pheromones[u][v] += pheromone_contribution
                self.pheromones[v][u] += pheromone_contribution  # Для неориентированных графов

