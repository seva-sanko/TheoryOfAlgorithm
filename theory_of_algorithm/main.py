import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import random
import time

variant = 39
day = 23
month = 3
year = 2005
n = 11 *  variant * day * month * year

print(n)

class NeumannCellularAutomaton:
    def __init__(self, width, height=None):
        if height is None:
            height = width
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

        self.rules = self._generate_rules_from_id(n)

    def _generate_rules_from_id(self, student_id):
        binary_str = bin(student_id)[2:]
        while len(binary_str) < 32:
            binary_str = '0' + binary_str
        rules_binary = binary_str[-32:]

        rules = {}
        for i in range(32):
            rules[i] = int(rules_binary[i])
            # rules[i] = int(rules_binary[31 - i])

        #rules[0] = 0

        # 00000011100010100110010010110101
        return rules
    '''
    A B C D E  F
    0 0 0 0 0  0
    0 0 0 0 1  0
    0 0 0 1 0  0
    0 0 0 1 1  0
    0 0 1 0 0  0
    0 0 1 0 1  0
    0 0 1 1 0  1
    0 0 1 1 1  1
    0 1 0 0 0  1
    0 1 0 0 1  0
    0 1 0 1 0  0
    0 1 0 1 1  0
    0 1 1 0 0  1
    0 1 1 0 1  0
    0 1 1 1 0  1
    0 1 1 1 1  0
    1 0 0 0 0  0
    1 0 0 0 1  1
    1 0 0 1 0  1
    1 0 0 1 1  0
    1 0 1 0 0  0
    1 0 1 0 1  1
    1 0 1 1 0  0
    1 0 1 1 1  0
    1 1 0 0 0  1
    1 1 0 0 1  0
    1 1 0 1 0  1
    1 1 0 1 1  1
    1 1 1 0 0  0
    1 1 1 0 1  1
    1 1 1 1 0  0
    1 1 1 1 1  1
    '''

    def get_neumann_neighbors(self, x, y):
        neighbors = []
        neighbors.append(self.grid[(y - 1) % self.height, x])  # верхний
        neighbors.append(self.grid[y, (x + 1) % self.width])  # правый
        neighbors.append(self.grid[(y + 1) % self.height, x])  # нижний
        neighbors.append(self.grid[y, (x - 1) % self.width])  # левый
        return neighbors

    def get_neighborhood_state(self, x, y):
        center = self.grid[y, x]
        neighbors = self.get_neumann_neighbors(x, y)

        state = center * 16  # центральная клетка (бит 4)
        state += neighbors[0] * 8  # верхний сосед (бит 3)
        state += neighbors[1] * 4  # правый сосед (бит 2)
        state += neighbors[2] * 2  # нижний сосед (бит 1)
        state += neighbors[3] * 1  # левый сосед (бит 0)
        return state

    def update(self):
        new_grid = np.zeros((self.height, self.width), dtype=int)

        for y in range(self.height):
            for x in range(self.width):
                neighborhood_state = self.get_neighborhood_state(x, y)
                new_grid[y, x] = self.rules[neighborhood_state]

        self.grid = new_grid

    def set_random_initial_state(self, density=0.5):
        self.grid = np.random.choice([0, 1], size=(self.height, self.width),
                                     p=[1 - density, density])


    def set_manual_initial_state(self, pattern):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x, center_y = self.width // 2, self.height // 2

        if pattern == "random":
            self.set_random_initial_state(0.5)

        elif pattern == "waves":
            for y in range(self.height):
                for x in range(self.width):
                    if (y // 2) % 3 == 0:
                        self.grid[y, x] = 1

        elif pattern == "checkerboard":
            cell_size = 2
            for y in range(self.height):
                for x in range(self.width):
                    if ((x // cell_size) + (y // cell_size)) % 2 == 0:
                        self.grid[y, x] = 1

        elif pattern == "spiral":
            size = min(self.width, self.height) // 3
            for i in range(size):
                angle = i * 0.3
                radius = i * 0.8
                x = int(center_x + radius * np.cos(angle))
                y = int(center_y + radius * np.sin(angle))
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y, x] = 1
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height and random.random() < 0.3:
                                self.grid[ny, nx] = 1

        elif pattern == "dots_grid":
            spacing = 5
            for y in range(0, self.height, spacing):
                for x in range(0, self.width, spacing):
                    if y < self.height and x < self.width:
                        self.grid[y, x] = 1

        elif pattern == "cross":
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
        if visualize:
            self.visualize_simulation(iterations)
        else:
            self.run_console_simulation(iterations)

    def run_console_simulation(self, iterations):
        print("Начальное состояние:")
        self.print_grid()

        print(f"\n{'Шаг':<6} {'Живые':<8} {'Плотность':<10}")
        print("-" * 25)

        for i in range(iterations + 1):
            if i > 0:
                self.update()

            live_cells = np.sum(self.grid)
            density = live_cells / (self.width * self.height)
            print(f"{i:<6} {live_cells:<8} {density:.4f}")

            if i < iterations:
                print(f"\nШаг {i + 1}:")
                self.print_grid()
                time.sleep(0.5)

    def print_grid(self):
        for row in self.grid:
            print(''.join(['█' if cell else ' ' for cell in row]))

    """
    def visualize_simulation(self, iterations):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Используем разные цветовые схемы
        cmap_stable = colors.ListedColormap(['white', 'blue', 'red', 'green'])

        # Для отслеживания стабильности
        history = [self.grid.copy()]
        stability_grid = np.zeros_like(self.grid)  # 0-неизмен, 1-измен, 2-стабилен, 3-осциллятор

        # Инициализируем отображения
        img = ax1.imshow(self.grid, cmap='binary', interpolation='nearest')
        ax1.set_title('Текущее состояние\n(белый=0, черный=1)')
        ax1.set_xticks([])
        ax1.set_yticks([])

        img_stable = ax2.imshow(stability_grid, cmap=cmap_stable, interpolation='nearest', vmin=0, vmax=3)
        ax2.set_title('Стабильность клеток')
        ax2.set_xticks([])
        ax2.set_yticks([])

        # Графики разных метрик
        line_state1, = ax3.plot([], [], 'b-', linewidth=2, label='Состояние 1')
        line_changes, = ax3.plot([], [], 'r-', linewidth=2, label='Изменения')
        line_stable, = ax3.plot([], [], 'g-', linewidth=2, label='Стабильные')

        ax3.set_xlabel('Шаг итерации')
        ax3.set_ylabel('Количество клеток')
        ax3.set_title('Динамика системы')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, iterations)
        ax3.legend()

        # История метрик
        state1_history = [np.sum(self.grid)]
        changes_history = [0]
        stable_history = [0]

        def animate(frame):
            nonlocal history, stability_grid

            if frame > 0:
                # Сохраняем предыдущее состояние
                previous_grid = history[-1].copy()

                # Обновляем автомат
                self.update()
                current_grid = self.grid.copy()
                history.append(current_grid)

                # Анализируем изменения и стабильность
                changes = (previous_grid != current_grid)
                num_changes = np.sum(changes)

                # Обновляем карту стабильности
                if frame >= 2:
                    # Клетка стабильна, если не менялась 2 шага
                    stable_cells = (history[-1] == history[-2]) & (history[-1] == history[-3])
                    # Клетка осциллирует, если меняется каждый шаг
                    oscillating = changes & (previous_grid != history[-3] if frame >= 3 else changes)

                    stability_grid = np.zeros_like(self.grid)
                    stability_grid[stable_cells & (current_grid == 1)] = 2  # Стабильные 1
                    stability_grid[stable_cells & (current_grid == 0)] = 3  # Стабильные 0
                    stability_grid[oscillating] = 1  # Осцилляторы

                current_state1 = np.sum(current_grid)
                current_stable = np.sum(stability_grid >= 2) if frame >= 2 else 0

                state1_history.append(current_state1)
                changes_history.append(num_changes)
                stable_history.append(current_stable)

            else:
                # Первый кадр
                current_state1 = state1_history[0]
                current_changes = 0
                current_stable = 0

            # Обновляем основное изображение
            img.set_array(self.grid)

            # Обновляем карту стабильности
            if frame >= 2:
                img_stable.set_array(stability_grid)

            # Обновляем графики
            x_data = list(range(frame + 1))
            line_state1.set_data(x_data, state1_history[:frame + 1])
            line_changes.set_data(x_data, changes_history[:frame + 1])
            line_stable.set_data(x_data, stable_history[:frame + 1])

            # Автоматически подбираем масштаб
            max_val = max(max(state1_history) if state1_history else 1,
                          max(changes_history) if changes_history else 1,
                          max(stable_history) if stable_history else 1)
            ax3.set_ylim(0, max(1, max_val * 1.1))

            # Обновляем аннотации
            if hasattr(animate, 'annotations'):
                for ann in animate.annotations:
                    ann.remove()

            animate.annotations = []
            if frame > 0:
                ann1 = ax3.annotate(f'1: {state1_history[-1]}',
                                    xy=(frame, state1_history[-1]), xytext=(5, 5),
                                    textcoords='offset points', color='blue',
                                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
                ann2 = ax3.annotate(f'Δ: {changes_history[-1]}',
                                    xy=(frame, changes_history[-1]), xytext=(5, -15),
                                    textcoords='offset points', color='red',
                                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.7))
                ann3 = ax3.annotate(f'S: {stable_history[-1]}',
                                    xy=(frame, stable_history[-1]), xytext=(5, -35),
                                    textcoords='offset points', color='green',
                                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7))
                animate.annotations = [ann1, ann2, ann3]

            return img, img_stable, line_state1, line_changes, line_stable

        # Создаем анимацию
        anim = animation.FuncAnimation(
            fig, animate, frames=iterations + 1,
            interval=500, repeat=False, blit=False
        )

        # Легенда для карты стабильности
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='white', label='Нестабильные'),
            Patch(facecolor='red', label='Осцилляторы'),
            Patch(facecolor='blue', label='Стабильные 1'),
            Patch(facecolor='green', label='Стабильные 0')
        ]
        ax2.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()

        # Сохраняем историю
        self.state1_history = state1_history
        self.changes_history = changes_history
        self.stable_history = stable_history

        """

    def visualize_simulation(self, iterations):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        cmap = colors.ListedColormap(['white', 'black'])

        img = ax1.imshow(self.grid, cmap=cmap, interpolation='nearest')
        ax1.set_title(f'Клеточный автомат (шаг 0)')
        ax1.set_xticks([])
        ax1.set_yticks([])

        line, = ax2.plot([], [], 'b-', linewidth=2)
        ax2.set_xlabel('Шаг итерации')
        ax2.set_ylabel('Количество клеток в состоянии 1')
        ax2.set_title('Динамика состояния 1')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, iterations)

        live_cells_history = [np.sum(self.grid)]

        def animate(frame):
            if frame > 0:
                self.update()
                current_live = np.sum(self.grid)
                live_cells_history.append(current_live)
            else:
                current_live = live_cells_history[0]

            img.set_array(self.grid)
            ax1.set_title(f'Клеточный автомат (шаг {frame})')

            x_data = list(range(frame + 1))
            line.set_data(x_data, live_cells_history[:frame + 1])

            if live_cells_history:
                max_live = max(live_cells_history)
                ax2.set_ylim(0, max(1, max_live * 1.1))

            if hasattr(animate, 'annotation'):
                animate.annotation.remove()

            if frame > 0:
                animate.annotation = ax2.annotate(f'{current_live}',
                                                  xy=(frame, current_live),
                                                  xytext=(5, 5), textcoords='offset points',
                                                  bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

            return img, line

        anim = animation.FuncAnimation(
            fig, animate, frames=iterations + 1,
            interval=500, repeat=False, blit=False
        )

        plt.tight_layout()
        plt.show()

        self.live_cells_history = live_cells_history



    def analyze_behavior(self, max_iterations=100):
        print("Расширенный анализ поведения автомата...")

        initial_grid = self.grid.copy()

        live_history = []
        density_history = []

        for i in range(max_iterations):
            live_cells = np.sum(self.grid)
            density = live_cells / (self.width * self.height)

            live_history.append(live_cells)
            density_history.append(density)

            self.update()

            if i > 0 and live_history[-1] == live_history[-2]:
                print(f"Стабилизация на шаге {i}: {live_cells} живых клеток")
                break

        self.grid = initial_grid

        self.plot_behavior_analysis(live_history, density_history, max_iterations)

        return live_history, density_history

    def plot_behavior_analysis(self, live_history, density_history, max_iterations):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        steps = list(range(len(live_history)))

        ax1.plot(steps, live_history, 'b-', linewidth=2, label='Живые клетки')
        ax1.set_xlabel('Шаг итерации')
        ax1.set_ylabel('Количество живых клеток')
        ax1.set_title('Динамика количества живых клеток')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.plot(steps, density_history, 'r-', linewidth=2, label='Плотность')
        ax2.set_xlabel('Шаг итерации')
        ax2.set_ylabel('Плотность')
        ax2.set_title('Динамика плотности')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        ax3.hist(live_history, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax3.set_xlabel('Количество живых клеток')
        ax3.set_ylabel('Частота')
        ax3.set_title('Распределение количества живых клеток')
        ax3.grid(True, alpha=0.3)

        if len(live_history) > 1:
            changes = [live_history[i] - live_history[i - 1] for i in range(1, len(live_history))]
            ax4.plot(steps[1:], changes, 'g-', linewidth=2, label='Изменение')
            ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5)
            ax4.set_xlabel('Шаг итерации')
            ax4.set_ylabel('Изменение количества клеток')
            ax4.set_title('Скорость изменения')
            ax4.grid(True, alpha=0.3)
            ax4.legend()

        plt.tight_layout()
        plt.show()

        print(f"\nСтатистика анализа:")
        print(f"Начальное количество: {live_history[0]}")
        print(f"Финальное количество: {live_history[-1]}")
        print(f"Максимальное количество: {max(live_history)}")
        print(f"Минимальное количество: {min(live_history)}")
        print(f"Среднее количество: {np.mean(live_history):.2f}")


def main():
    print("Двумерный клеточный автомат с окрестностью фон Неймана")
    print("Функция: 59350005")

    try:
        width = int(input("Введите ширину поля: ") or 100)
        iterations = int(input("Введите количество итераций: ") or 100)
    except ValueError:
        print("Ошибка: введите целые числа")
        return

    automaton = NeumannCellularAutomaton(width)

    print("\nВыберите начальное состояние:")
    print("1 - Случайное распределение")
    print("2 - Волны")
    print("3 - Шахматная доска")
    print("4 - Спираль")
    print("5 - Сетка из точек")
    print("6 - Крест")
    print("7 - Случайное плотное (70%)")
    print("8 - Случайное разреженное (30%)")

    choice = input("Ваш выбор (1-8): ") or "1"

    patterns = {
        "1": "random",
        "2": "waves",
        "3": "checkerboard",
        "4": "spiral",
        "5": "dots_grid",
        "6": "cross",
        "7": "random_dense",
        "8": "random_sparse"
    }

    if choice in patterns:
        pattern = patterns[choice]
        if pattern.startswith("random"):
            density = 0.7 if pattern == "random_dense" else 0.3 if pattern == "random_sparse" else 0.5
            automaton.set_random_initial_state(density)
        else:
            automaton.set_manual_initial_state(pattern)
    else:
        print("Неверный выбор, используется случайное распределение")
        automaton.set_random_initial_state(0.5)

    display_mode = input("Режим отображения (1 - консоль, 2 - графика): ") or "2"

    if display_mode == "1":
        automaton.run_simulation(iterations, visualize=False)
    else:
        automaton.run_simulation(iterations, visualize=True)

    analyze = input("Провести расширенный анализ поведения? (y/n): ")
    if analyze.lower() == 'y':
        automaton.analyze_behavior(iterations)


if __name__ == "__main__":
    main()