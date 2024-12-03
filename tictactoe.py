import numpy as np

BOARD_SIZE = 20  # Размер доски
WIN_CONDITION = 5  # Количество символов в ряд для победы
MAX_DEPTH = 3  # Максимальная глубина поиска

# Инициализация доски
board = np.full((BOARD_SIZE, BOARD_SIZE), '.', dtype=str)

def print_board():
    """Печатает игровое поле."""
    print("0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19")
    for i in range(BOARD_SIZE):
        for row in board:
            print(i + " " " ".join(row))
        print()

def check_win(player):
    """Проверяет, выиграл ли игрок."""
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Горизонталь
            if j <= BOARD_SIZE - WIN_CONDITION and all(board[i, j + k] == player for k in range(WIN_CONDITION)):
                return True
            # Вертикаль
            if i <= BOARD_SIZE - WIN_CONDITION and all(board[i + k, j] == player for k in range(WIN_CONDITION)):
                return True
            # Диагональ (слева направо)
            if i <= BOARD_SIZE - WIN_CONDITION and j <= BOARD_SIZE - WIN_CONDITION and all(
                    board[i + k, j + k] == player for k in range(WIN_CONDITION)):
                return True
            # Диагональ (справа налево)
            if i <= BOARD_SIZE - WIN_CONDITION and j >= WIN_CONDITION - 1 and all(
                    board[i + k, j - k] == player for k in range(WIN_CONDITION)):
                return True
    return False

def evaluate(player):
    """Оценочная функция для компьютера."""
    opponent = 'X' if player == 'O' else 'O'
    if check_win(player):
        return 1000  # Победа компьютера
    if check_win(opponent):
        return -1000  # Победа игрока
    return 0  # Ничья

def is_moves_left():
    """Проверяет, есть ли свободные клетки."""
    return np.any(board == '.')

def get_possible_moves():
    """Возвращает список доступных ходов вблизи занятых клеток."""
    moves = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i, j] != '.':
                for ni in range(max(0, i - 1), min(BOARD_SIZE, i + 2)):
                    for nj in range(max(0, j - 1), min(BOARD_SIZE, j + 2)):
                        if board[ni, nj] == '.':
                            moves.add((ni, nj))
    return list(moves)

def minimax(depth, is_max, alpha, beta, player):
    """Алгоритм Minimax с альфа-бета отсечением."""
    opponent = 'X' if player == 'O' else 'O'
    score = evaluate(player)

    # Базовые случаи
    if score == 1000:
        return score - depth
    if score == -1000:
        return score + depth
    if not is_moves_left() or depth == MAX_DEPTH:
        return 0

    possible_moves = get_possible_moves()

    # Максимизирующий игрок (компьютер)
    if is_max:
        max_eval = -np.inf
        for i, j in possible_moves:
            board[i, j] = player
            eval = minimax(depth + 1, False, alpha, beta, player)
            board[i, j] = '.'  # Отменяем ход

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Альфа-бета отсечение
        return max_eval

    # Минимизирующий игрок (человек)
    else:
        min_eval = np.inf
        for i, j in possible_moves:
            board[i, j] = opponent
            eval = minimax(depth + 1, True, alpha, beta, player)
            board[i, j] = '.'  # Отменяем ход

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Альфа-бета отсечение
        return min_eval

def find_best_move(player):
    """Находит лучший ход для компьютера."""
    best_val = -np.inf
    best_move = (-1, -1)
    possible_moves = get_possible_moves()
    for i, j in possible_moves:
        board[i, j] = player
        move_val = minimax(0, False, -np.inf, np.inf, player)
        board[i, j] = '.'
        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val
    return best_move

def player_move():
    """Ход игрока."""
    while True:
        try:
            x, y = map(int, input("Введите ваш ход (строка и столбец через пробел): ").split())
            if board[x, y] == '.':
                board[x, y] = 'X'
                break
            else:
                print("Эта клетка занята. Попробуйте снова!")
        except (ValueError, IndexError):
            print("Некорректный ввод. Введите два числа от 0 до", BOARD_SIZE - 1)

def main():
    print("Вы играете за 'X', компьютер — за 'O'.")
    print_board()

    while True:
        # Ход игрока
        player_move()
        print_board()
        if check_win('X'):
            print("Поздравляем! Вы выиграли!")
            break
        if not is_moves_left():
            print("Ничья!")
            break

        # Ход компьютера
        print("Компьютер думает...")
        ai_move = find_best_move('O')
        board[ai_move] = 'O'
        print_board()
        if check_win('O'):
            print("Компьютер выиграл! Удачи в следующий раз!")
            break
        if not is_moves_left():
            print("Ничья!")
            break

if __name__ == "__main__":
    main()
