import timeit
import matplotlib.pyplot as plt
from collections import deque, namedtuple
from typing import Any, Callable, Dict, List, Optional

# Эти функции уже были даны в задании
Node = namedtuple('Node', ['value', 'left', 'right'])

def build_tree_iterative(
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[Any], Any] = lambda x: x * 4,
    right_branch: Callable[[Any], Any] = lambda x: x + 1
) -> Dict[str, Any]:
    """Нерекурсивный метод (с очередью)"""
    if height <= 0:
        return {}
    tree = {'value': root, 'left': None, 'right': None}
    queue = deque()
    queue.append((tree, 1))  # (узел, текущий уровень)
    while queue:
        current_node, current_level = queue.popleft()
        if current_level >= height:
            continue
        # Создаем левого потомка
        left_value = left_branch(current_node['value'])
        current_node['left'] = {'value': left_value, 'left': None, 'right': None}
        queue.append((current_node['left'], current_level + 1))
        # Создаем правого потомка
        right_value = right_branch(current_node['value'])
        current_node['right'] = {'value': right_value, 'left': None, 'right': None}
        queue.append((current_node['right'], current_level + 1))
    return tree

def build_tree_recursive(
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[Any], Any] = lambda x: x * 4,
    right_branch: Callable[[Any], Any] = lambda x: x + 1
) -> Dict[str, Any]:
    """Рекурсивный метод"""
    if height <= 0:
        return {}
    if height == 1:
        return {'value': root, 'left': None, 'right': None}
    # Рекурсивно создаем левое поддерево
    left_subtree = build_tree_recursive(
        height=height - 1,
        root=left_branch(root),
        left_branch=left_branch,
        right_branch=right_branch
    )
    # Рекурсивно создаем правое поддерево
    right_subtree = build_tree_recursive(
        height=height - 1,
        root=right_branch(root),
        left_branch=left_branch,
        right_branch=right_branch
    )
    return {
        'value': root,
        'left': left_subtree,
        'right': right_subtree
    }

# Функция для подсчета количества узлов в дереве
def count_nodes(tree):
    """Простая функция для подсчета узлов в дереве"""
    if not tree:
        return 0
    count = 1  # считаем текущий узел
    if tree['left']:
        count += count_nodes(tree['left'])
    if tree['right']:
        count += count_nodes(tree['right'])
    return count

# Функция для замера времени
def measure_time(func, height, number=100):
    """Замеряет время выполнения функции"""
    times = timeit.repeat(
        lambda: func(height=height, root=4, left_branch=lambda x: x*4, right_branch=lambda x: x+1),
        number=number,
        repeat=3
    )
    return min(times)  # берем минимальное время

if __name__ == "__main__":
    # Тестируем разные высоты
    heights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    iter_times = []
    rec_times = []

    print("\nВысота | Узлов | Нерекурсивный | Рекурсивный | Во сколько раз")
    print("-" * 65)
    for h in heights:
        # Считаем сколько узлов должно быть в дереве
        nodes = 2**h - 1
        # Замеряем время
        t_iter = measure_time(build_tree_iterative, h)
        t_rec = measure_time(build_tree_recursive, h)
        iter_times.append(t_iter)
        rec_times.append(t_rec)
        # Сравниваем
        if t_rec > t_iter:
            faster = f"в {t_rec/t_iter:.2f} раза быстрее итер"
        else:
            faster = f"в {t_iter/t_rec:.2f} раза быстрее рекур"
        print(f"{h:6} | {nodes:5} | {t_iter:.8f} | {t_rec:.8f} | {faster}")

    # Считаем среднее значение для последних нескольких замеров
    avg_ratio = sum(rec_times[i]/iter_times[i] for i in range(len(heights)-3, len(heights))) / 3
    print(f"\nДля больших деревьев рекурсивный метод медленнее примерно в {avg_ratio:.2f} раза")

    # Рисуем график
    plt.figure(figsize=(12, 5))

    # График 1: обычный
    plt.subplot(1, 2, 1)
    plt.plot(heights, iter_times, 'o-', label='Нерекурсивный', linewidth=2, color='blue')
    plt.plot(heights, rec_times, 's-', label='Рекурсивный', linewidth=2, color='red')
    plt.xlabel('Высота дерева')
    plt.ylabel('Время построения дерева')
    plt.title('Зависимость времени от высоты дерева')
    plt.legend()
    plt.grid(True)