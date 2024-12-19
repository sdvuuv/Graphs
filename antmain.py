import numpy as np
import matplotlib.pyplot as plt
import random

class Ant:
    def __init__(self, num_nodes, start, end, alpha=1.0, beta=2.0):
        # Инициализация муравья
        self.num_nodes = num_nodes  # Общее количество узлов
        self.start = start  # Стартовый узел
        self.end = end  # Конечный узел
        self.tour = []  # Тур муравья
        self.distance = 0  # Расстояние тура
        self.alpha = alpha  # Влияние феромонов
        self.beta = beta  # Влияние видимости

    def construct_tour(self, pheromones, visibility, distances):
        # Построение маршрута
        self.tour = [self.start]
        current_node = self.start
        unvisited = set(range(self.num_nodes)) - {self.start}

        while current_node != self.end:
            if not unvisited and current_node != self.end:
                self.tour.append(self.end)
                break

            # Определяем кандидатов для посещения
            candidates = list(unvisited) + ([self.end] if self.end not in self.tour else [])
            probabilities = self.calculate_probabilities(current_node, candidates, pheromones, visibility)

            # Выбираем следующий узел
            next_node = np.random.choice(candidates, p=probabilities)
            self.tour.append(next_node)
            current_node = next_node

            if next_node in unvisited:
                unvisited.remove(next_node)

        # Вычисляем общее расстояние
        self.distance = sum(distances[self.tour[i]][self.tour[i + 1]] for i in range(len(self.tour) - 1))

    def calculate_probabilities(self, current, candidates, pheromones, visibility):
        # Вычисление вероятностей перехода
        weights = [(pheromones[current][c] ** self.alpha) * (visibility[current][c] ** self.beta) for c in candidates]
        total = sum(weights)
        return [w / total if total > 0 else 1 / len(candidates) for w in weights]


def ant_colony_optimization(num_ants, iterations, evaporation, start, end, distances):
    # Алгоритм муравьиной колонии
    num_nodes = len(distances)
    pheromones = np.ones((num_nodes, num_nodes))  # Матрица феромонов
    visibility = np.where(distances > 0, 1 / distances, 0)  # Матрица видимости

    best_tour = None
    best_distance = float('inf')

    history = {
        'distances': [],  # История расстояний
        'pheromones': [],  # История феромонов
    }

    for _ in range(iterations):
        ants = [Ant(num_nodes, start, end) for _ in range(num_ants)]

        for ant in ants:
            ant.construct_tour(pheromones, visibility, distances)
            if ant.distance < best_distance:
                best_distance = ant.distance
                best_tour = ant.tour

        # Испарение феромонов
        pheromones *= (1 - evaporation)

        # Обновление феромонов
        for ant in ants:
            for i in range(len(ant.tour) - 1):
                a, b = ant.tour[i], ant.tour[i + 1]
                pheromones[a][b] += 1 / ant.distance

        history['distances'].append(best_distance)
        history['pheromones'].append(np.mean(pheromones))

    return best_tour, best_distance, history


def plot_results(history):
    # Построение графиков
    plt.figure(figsize=(6, 6))

    plt.subplot(1, 1, 1)
    plt.plot(history['pheromones'], label='Средний уровень феромонов', color='red')
    plt.title('Уровень феромонов по итерациям')
    plt.xlabel('Итерация')
    plt.ylabel('Уровень феромонов')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    # Главная функция программы
    distances = np.array([
            [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
            [120, 0, 22, 32, 42, 52, 602, 72, 82, 92, 102, 112],
            [140, 24, 0, 34, 44, 54, 64, 74, 84, 94, 104, 114],
            [160, 26, 36, 0, 460, 56, 66, 76, 86, 96, 106, 116],
            [180, 28, 38, 48, 0, 58, 68, 78, 88, 98, 108, 118],
            [200, 30, 40, 50, 60, 0, 70, 80, 90, 100, 110, 120],
            [22, 302, 420, 52, 62, 72, 0, 82, 92, 102, 112, 122],
            [24, 34, 44, 54, 64, 74, 84, 0, 94, 104, 114, 124],
            [26, 36, 46, 56, 66, 76, 86, 96, 0, 106, 116, 126],
            [28, 38, 48, 58, 68, 78, 88, 98, 108, 0, 118, 128],
            [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 0, 130],
            [32, 42, 52, 62, 72, 82, 92, 102, 112, 122, 132, 0]
        ])

    start, end = 0, 3
    num_ants = 10
    iterations = 50
    evaporation = 0.1

    best_tour, best_distance, history = ant_colony_optimization(num_ants, iterations, evaporation, start, end, distances)

    print(f"Лучший маршрут: {best_tour}")
    print(f"Лучшее расстояние: {best_distance:.2f}")

    plot_results(history)


if __name__ == "__main__":
    main()
