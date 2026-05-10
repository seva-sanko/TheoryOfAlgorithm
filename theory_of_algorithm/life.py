import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import time


class GameOfLife:
    def __init__(self, width, height=None):
        if height is None:
            height = width
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def get_moore_neighbors(self, x, y):
        neighbors = []

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                neighbors.append(self.grid[ny, nx])

        return neighbors

    def count_live_neighbors(self, x, y):
        """Подсчет живых соседей"""
        neighbors = self.get_moore_neighbors(x, y)
        return sum(neighbors)

    def update(self):
        """Обновление состояния по правилам игры в жизнь"""
        new_grid = np.zeros((self.height, self.width), dtype=int)

        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                current_state = self.grid[y, x]

                # Правила игры в жизнь:
                # 1. Живая клетка с 2 или 3 живыми соседями выживает
                # 2. Мертвая клетка с ровно 3 живыми соседями оживает
                # 3. В остальных случаях клетка умирает или остается мертвой

                if current_state == 1:  # Живая клетка
                    if live_neighbors == 2 or live_neighbors == 3:
                        new_grid[y, x] = 1  # Выживает
                    else:
                        new_grid[y, x] = 0  # Умирает от одиночества или перенаселения
                else:  # Мертвая клетка
                    if live_neighbors == 3:
                        new_grid[y, x] = 1  # Оживает
                    else:
                        new_grid[y, x] = 0  # Остается мертвой

        self.grid = new_grid

    def set_random_initial_state(self, density=0.3):
        """Установка случайного начального состояния"""
        self.grid = np.random.choice([0, 1], size=(self.height, self.width),
                                     p=[1 - density, density])

    def set_manual_initial_state(self, pattern):
        """Установка начального состояния вручную"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x, center_y = self.width // 2, self.height // 2

        if pattern == "glider":
            # Планер для окрестности фон Неймана
            self.grid[center_y, center_x] = 1
            self.grid[center_y - 1, center_x] = 1
            self.grid[center_y, center_x + 1] = 1
            self.grid[center_y + 1, center_x] = 1
            self.grid[center_y, center_x - 1] = 1

        elif pattern == "dart":
            # Дартс
            coords = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (1, 2)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "turtle":
            # Черепаха
            coords = [(0, 0), (2, 0), (-1, 1), (3, 1), (0, 2), (1, 2), (2, 2)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "french_kiss":
            # Французский поцелуй
            coords = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (2, 2), (1, 2), (2, 1)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "weekend":
            # Уикенд
            coords = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "spider":
            # Паук
            coords = [(0, 0), (1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "bipole":
            # Биполяр
            for i in range(3):
                self.grid[center_y, center_x + i] = 1
                self.grid[center_y, center_x - i] = 1

        elif pattern == "tripole":
            # Триполяр
            for i in range(3):
                self.grid[center_y + i, center_x] = 1
                self.grid[center_y - i, center_x] = 1
                self.grid[center_y, center_x + i] = 1

        elif pattern == "scrubber":
            # Скруббер
            coords = [(0, 0), (1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3), (2, 3)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "muttering_moat":
            # Бормочущий ров
            coords = [(0, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "glasses":
            # Очки
            coords = [(0, 0), (1, 0), (3, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (3, 3)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "babbling_brook":
            # Бормочущий ручей
            coords = [(0, 0), (1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3), (2, 3)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "unix":
            # UNIX
            coords = [(0, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3)]
            for dx, dy in coords:
                self.grid[center_y + dy, center_x + dx] = 1

        elif pattern == "cross":
            # Крест
            self.grid[center_y, center_x] = 1
            self.grid[center_y - 1, center_x] = 1
            self.grid[center_y + 1, center_x] = 1
            self.grid[center_y, center_x - 1] = 1
            self.grid[center_y, center_x + 1] = 1

        elif pattern == "random_dense":
            self.set_random_initial_state(0.7)
        elif pattern == "random_sparse":
            self.set_random_initial_state(0.3)

    def run_simulation(self, iterations, visualize=True):
        """Запуск симуляции"""
        if visualize:
            self.visualize_simulation(iterations)
        else:
            self.run_console_simulation(iterations)

    def run_console_simulation(self, iterations):
        """Запуск симуляции в консоли"""
        print("Начальное состояние:")
        self.print_grid()

        for i in range(iterations):
            self.update()
            print(f"\nШаг {i + 1}:")
            self.print_grid()
            time.sleep(0.3)

    def print_grid(self):
        """Вывод сетки в консоль"""
        for row in self.grid:
            print(''.join(['█' if cell else ' ' for cell in row]))

    def visualize_simulation(self, iterations):
        """Визуализация симуляции с помощью matplotlib"""
        fig, ax = plt.subplots(figsize=(10, 10))
        cmap = colors.ListedColormap(['white', 'black'])

        # Настройка отображения
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        def animate(frame):
            if frame > 0:
                self.update()
            ax.clear()
            ax.imshow(self.grid, cmap=cmap, interpolation='nearest')
            ax.set_title(f'Игра в жизнь (поколение {frame})')
            ax.set_xticks([])
            ax.set_yticks([])

            # Добавляем сетку для лучшей видимости
            ax.grid(which='both', color='lightgray', linewidth=0.5)
            ax.set_xticks(np.arange(-0.5, self.width, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, self.height, 1), minor=True)

        anim = animation.FuncAnimation(fig, animate, frames=iterations + 1,
                                       interval=200, repeat=False)
        plt.tight_layout()
        plt.show()

    def analyze_patterns(self, max_iterations=100):
        """Анализ паттернов и поведения"""
        print("Анализ игры в жизнь...")

        initial_state = self.grid.copy()
        states_history = [initial_state.copy()]
        density_history = [np.mean(initial_state)]
        population_history = [np.sum(initial_state)]

        print(f"Поколение 0: клеток = {population_history[0]}, плотность = {density_history[0]:.3f}")

        for i in range(1, max_iterations + 1):
            self.update()
            current_state = self.grid.copy()

            population = np.sum(current_state)
            density = np.mean(current_state)

            population_history.append(population)
            density_history.append(density)
            states_history.append(current_state.copy())

            print(f"Поколение {i}: клеток = {population}, плотность = {density:.3f}")

            # Проверка на стабильность
            if np.array_equal(current_state, states_history[-2]):
                print(f"Достигнуто стабильное состояние на поколении {i}")
                return density_history, population_history, "stable"

            # Проверка на периодичность
            for j in range(len(states_history) - 2):
                if np.array_equal(current_state, states_history[j]):
                    period = i - j
                    print(f"Обнаружена периодичность с периодом {period}")
                    return density_history, population_history, f"periodic_{period}"

            # Проверка на вымирание
            if population == 0:
                print(f"Все клетки вымерли на поколении {i}")
                return density_history, population_history, "extinct"

        print(f"Достигнут предел в {max_iterations} поколений")
        return density_history, population_history, "complex"


def main():
    print("Игра в жизнь Конвея")
    print("===================")

    # Ввод параметров
    try:
        width = int(input("Введите ширину поля (рекомендуется 30-100): ") or "50")
        height = int(input(f"Введите высоту поля [{width}]: ") or width)
        iterations = int(input("Введите количество поколений: ") or "100")
    except ValueError:
        print("Ошибка: введите целые числа")
        return

    # Создание автомата
    game = GameOfLife(width, height)

    print("\nВыберите начальное состояние:")
    print("1 - Случайное (плотность 0.5)")
    print("2 - Случайное плотное (0.7)")
    print("3 - Случайное разреженное (0.3)")
    print("4 - Планер")
    print("5 - Дартс")
    print("6 - Черепаха")
    print("7 - Французский поцелуй")
    print("8 - Уикенд")
    print("9 - Паук")
    print("10 - Биполяр")
    print("11 - Триполяр")
    print("12 - Скруббер")
    print("13 - Бормочущий ров")
    print("14 - Очки")
    print("15 - Бормочущий ручей")
    print("16 - UNIX")
    print("17 - Крест")

    choice = input("Ваш выбор (1-17): ") or "1"

    patterns = {
        "1": ("random", 0.5),
        "2": ("random_dense", 0.7),
        "3": ("random_sparse", 0.3),
        "4": "glider",
        "5": "dart",
        "6": "turtle",
        "7": "french_kiss",
        "8": "weekend",
        "9": "spider",
        "10": "bipole",
        "11": "tripole",
        "12": "scrubber",
        "13": "muttering_moat",
        "14": "glasses",
        "15": "babbling_brook",
        "16": "unix",
        "17": "cross"
    }

    if choice in patterns:
        pattern = patterns[choice]
        if isinstance(pattern, tuple):
            game.set_random_initial_state(pattern[1])
        else:
            game.set_manual_initial_state(pattern)
    else:
        print("Неверный выбор, используется случайное состояние")
        game.set_random_initial_state(0.5)

    # Выбор режима отображения
    display_mode = input("Режим отображения (1 - консоль, 2 - графика [2]): ") or "2"

    if display_mode == "1":
        game.run_simulation(iterations, visualize=False)
    else:
        game.run_simulation(iterations, visualize=True)

    # Анализ поведения
    analyze = input("Провести анализ поведения? (y/N): ") or "n"
    if analyze.lower() == 'y':
        density_history, population_history, behavior = game.analyze_patterns()

        # Визуализация статистики
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.plot(population_history, 'b-', linewidth=2)
        plt.title('Количество живых клеток')
        plt.xlabel('Поколение')
        plt.ylabel('Клеток')
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(density_history, 'r-', linewidth=2)
        plt.title('Плотность населения')
        plt.xlabel('Поколение')
        plt.ylabel('Плотность')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        print(f"\nТип поведения: {behavior}")


if __name__ == "__main__":
    main()