import numpy as np
from typing import Tuple, Optional, List
import time

class Game:
    def __init__(self, size: int = 20, win_length: int = 5):
        """
        Инициализация игры.

        :param size: Размер игрового поля (размер x размер).
        :param win_length: Количество фишек в ряд, необходимых для победы.
        """
        self.size = size
        self.win_length = win_length
        self.board = np.zeros((size, size), dtype=int)  # Создаём игровое поле
        self.current_player = 1  # Текущий игрок: 1 - человек, -1 - компьютер
        self.move_count = 0  # Количество сделанных ходов

        # Определение весов для оценки комбинаций
        self.weights = {
            5: 1000000000,    # Пять в ряд
            4: 100000000,     # Открытая "четвёрка"
            '4b': 1000000,    # Заблокированная "четвёрка"
            3: 100000,        # Открытая "тройка"
            '3b': 10000,      # Заблокированная "тройка"
            2: 1000,          # Открытая "двойка"
            '2b': 100         # Заблокированная "двойка"
        }

        # Направления для проверки последовательностей
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Кэш для хранения уже проверенных комбинаций
        self.pattern_cache = {}

    def find_winning_move(self, player: int) -> Optional[Tuple[int, int]]:
        """
        Найти выигрышный ход для указанного игрока, если он существует.

        :param player: Игрок, для которого проверяется ход (1 или -1).
        :return: Координаты выигрышного хода или None, если такого хода нет.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.board[i][j] = player
                    if self.is_winner(player):
                        self.board[i][j] = 0
                        return (i, j)
                    self.board[i][j] = 0
        return None

    def check_sequence(self, x: int, y: int, dx: int, dy: int, player: int) -> Tuple[int, bool]:
        """
        Проверить длину и открытость последовательности, начиная с (x, y) в заданном направлении.

        :param x: Начальная координата x.
        :param y: Начальная координата y.
        :param dx: Направление по x.
        :param dy: Направление по y.
        :param player: Игрок, для которого проверяется последовательность (1 или -1).
        :return: Кортеж (длина последовательности, открыта ли последовательность).
        """
        key = (x, y, dx, dy, player)
        if key in self.pattern_cache:
            return self.pattern_cache[key]

        count = 1
        blocked_ends = 0

        x1, y1 = x + dx, y + dy
        while 0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == player:
            count += 1
            x1 += dx
            y1 += dy
        if not (0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == 0):
            blocked_ends += 1

        x1, y1 = x - dx, y - dy
        while 0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == player:
            count += 1
            x1 -= dx
            y1 -= dy
        if not (0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == 0):
            blocked_ends += 1

        result = (count, blocked_ends < 2)
        self.pattern_cache[key] = result
        return result

    def evaluate_position(self, x: int, y: int, player: int) -> int:
        """
        Оценить очки за размещение фишки в (x, y) для заданного игрока.

        :param x: Координата x.
        :param y: Координата y.
        :param player: Игрок (1 или -1).
        :return: Очки за указанную позицию.
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return 0

        score = 0
        for dx, dy in self.directions:
            length, is_open = self.check_sequence(x, y, dx, dy, player)
            if length >= self.win_length:
                score += self.weights[5]
            elif length == 4:
                score += self.weights[4] if is_open else self.weights['4b']
            elif length == 3:
                score += self.weights[3] if is_open else self.weights['3b']
            elif length == 2:
                score += self.weights[2] if is_open else self.weights['2b']
        return score

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Получить список допустимых ходов, отсортированных по оценке.

        :return: Список допустимых ходов в формате (x, y).
        """
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)]

        winning_move = self.find_winning_move(self.current_player)
        if winning_move:
            return [winning_move]

        blocking_move = self.find_winning_move(-self.current_player)
        if blocking_move:
            return [blocking_move]

        moves = []
        seen = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    for di in range(-2, 3):
                        for dj in range(-2, 3):
                            ni, nj = i + di, j + dj
                            if (ni, nj) not in seen and 0 <= ni < self.size and 0 <= nj < self.size and self.board[ni][nj] == 0:
                                attack_score = self.evaluate_position(ni, nj, self.current_player)
                                defense_score = self.evaluate_position(ni, nj, -self.current_player)
                                score = max(attack_score, defense_score)
                                moves.append((score, (ni, nj)))
                                seen.add((ni, nj))

        moves.sort(reverse=True)
        return [move for _, move in moves[:10]]

    def evaluate_board(self) -> int:
        """
        Оценить текущее состояние игрового поля.

        :return: Итоговая оценка поля.
        """
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if self.board[i][j] == self.current_player:
                        score += self.evaluate_position(i, j, self.current_player)
                    else:
                        score -= self.evaluate_position(i, j, -self.current_player)
        return score

    def is_winner(self, player: int) -> bool:
        """
        Проверить, выиграл ли указанный игрок.

        :param player: Игрок для проверки (1 или -1).
        :return: True, если игрок выиграл, иначе False.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    for dx, dy in self.directions:
                        count = 1
                        x1, y1 = i + dx, j + dy
                        while 0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == player:
                            count += 1
                            if count >= self.win_length:
                                return True
                            x1 += dx
                            y1 += dy

                        x1, y1 = i - dx, j - dy
                        while 0 <= x1 < self.size and 0 <= y1 < self.size and self.board[x1][y1] == player:
                            count += 1
                            if count >= self.win_length:
                                return True
                            x1 -= dx
                            y1 -= dy
        return False

    def make_move(self, x: int, y: int) -> bool:
        """
        Сделать ход для текущего игрока в указанных координатах.

        :param x: Координата x хода.
        :param y: Координата y хода.
        :return: True, если ход валиден, иначе False.
        """
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
            self.board[x][y] = self.current_player
            self.move_count += 1
            self.pattern_cache.clear()
            return True
        return False

    def get_ai_move(self) -> Tuple[int, int]:
        """
        Получить следующий ход ИИ.

        :return: Координаты хода ИИ.
        """
        winning_move = self.find_winning_move(self.current_player)
        if winning_move:
            return winning_move

        blocking_move = self.find_winning_move(-self.current_player)
        if blocking_move:
            return blocking_move

        valid_moves = self.get_valid_moves()
        return valid_moves[0] if valid_moves else (0, 0)

    def print_board(self):
        """
        Отобразить текущее состояние игрового поля.
        """

        symbols = {0: '.', 1: 'X', -1: 'O'}
        print('   ', end='')
        for i in range(self.size):
            print(f'{i:2}', end=' ')
        print()

        for i in range(self.size):
            print(f'{i:2} ', end='')
            for j in range(self.size):
                print(f' {symbols[self.board[i][j]]}', end=' ')
            print()

def play_game():

    game = Game()

    mode = input("\nВыберите режим:\n1 - Игрок ходит первым\n2 - Компьютер ходит первым\nВведите 1 или 2: ")
    while mode not in ['1', '2']:
        print("Некорректный выбор! Пожалуйста, выберите 1 или 2.")
        mode = input("Выберите режим:\n1 - Игрок ходит первым\n2 - Компьютер ходит первым\nВведите 1 или 2: ")

    if mode == '2':
        game.current_player = -1

    while True:
        game.print_board()

        if game.current_player == 1:
            try:
                row = int(input("Введите номер строки: "))
                col = int(input("Введите номер столбца: "))
                if not game.make_move(row, col):
                    print("Недопустимый ход! Попробуйте снова.")
                    continue
            except ValueError:
                print("Пожалуйста, введите числа!")
                continue
        else:
            print("Компьютер думает...")
            start_time = time.time()
            row, col = game.get_ai_move()
            think_time = time.time() - start_time
            game.make_move(row, col)
            print(f"Компьютер походил: {row}, {col} (время: {think_time:.2f}с)")

        if game.is_winner(game.current_player):
            game.print_board()
            winner = "Игрок" if game.current_player == 1 else "Компьютер"
            print(f"{winner} победил!")
            break

        if game.move_count == game.size * game.size:
            game.print_board()
            print("Ничья!")
            break

        game.current_player *= -1

if __name__ == "__main__":
    play_game()
