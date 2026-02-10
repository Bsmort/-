from collections import deque, namedtuple
from typing import Any, Callable, Dict, List, Optional, Union

Node = namedtuple('Node', ['value', 'left', 'right'])

def gen_bin_tree(
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[Any], Any] = lambda x: x * 4,
    right_branch: Callable[[Any], Any] = lambda x: x + 1
) -> Dict[str, Any]:
    """Генерирует бинарное дерево нерекурсивным способом."""
    if height <= 0:
        return {}
    """Создаем корневой узел"""
    tree_structure = {'value': root, 'left': None, 'right': None}
    """Очередь для обхода узлов в ширину"""
    queue = deque()
    """(узел, текущий уровень)"""
    queue.append((tree_structure, 1))  
    while queue:
        current_node, current_level = queue.popleft()
        """Если достигли максимальной высоты, прекращаем создавать потомков"""
        if current_level >= height:
            continue
        """Создаем левого потомка"""
        left_value = left_branch(current_node['value'])
        current_node['left'] = {'value': left_value, 'left': None, 'right': None}
        queue.append((current_node['left'], current_level + 1))
        """Создаем правого потомка"""
        right_value = right_branch(current_node['value'])
        current_node['right'] = {'value': right_value, 'left': None, 'right': None}
        queue.append((current_node['right'], current_level + 1))
    return tree_structure


def gen_bin_tree_list(
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[Any], Any] = lambda x: x * 4,
    right_branch: Callable[[Any], Any] = lambda x: x + 1
) -> List[Optional[int]]:
    """Генерирует бинарное дерево в виде списка (массива)."""
    if height <= 0:
        return []
    """Максимальное количество узлов в полном бинарном дереве высоты height"""
    max_nodes = 2 ** height - 1
    tree_list = [None] * max_nodes
    """Очередь для обхода: (индекс_узла, значение_узла, уровень)"""
    queue = deque()
    queue.append((0, root, 1))
    while queue:
        index, value, level = queue.popleft()
        tree_list[index] = value
        if level >= height:
            continue
        """Вычисляем значения потомков"""
        left_value = left_branch(value)
        right_value = right_branch(value)
        """Вычисляем индексы потомков"""
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        """Добавляем потомков в очередь"""
        if left_index < max_nodes:
            queue.append((left_index, left_value, level + 1))
        if right_index < max_nodes:
            queue.append((right_index, right_value, level + 1))
    return tree_list


def gen_bin_tree_namedtuple(
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[Any], Any] = lambda x: x * 4,
    right_branch: Callable[[Any], Any] = lambda x: x + 1
) -> Optional[Node]:
    """Генерирует бинарное дерево с использованием namedtuple."""
    if height <= 0:
        return None
    """Очередь для обхода: (родительский namedtuple, значение, уровень)"""
    queue = deque()
    """Создаем корневой узел"""
    root_node = Node(value=root, left=None, right=None)
    queue.append((root_node, root, 1))
    """Словарь для связи значений с их узлами (для обновления)"""
    nodes_dict = {id(root_node): root_node}
    while queue:
        parent_node, parent_value, level = queue.popleft()
        if level >= height:
            continue
        """Вычисляем значения потомков"""
        left_value = left_branch(parent_value)
        right_value = right_branch(parent_value)
        """Создаем узлы-потомки"""
        left_node = Node(value=left_value, left=None, right=None)
        right_node = Node(value=right_value, left=None, right=None)
        """Обновляем родительский узел (namedtuple неизменяем, создаем новый)"""
        new_parent_node = Node(
            value=parent_node.value,
            left=left_node,
            right=right_node
        )
        """Обновляем словарь"""
        nodes_dict[id(new_parent_node)] = new_parent_node
        """Добавляем потомков в очередь"""
        queue.append((left_node, left_value, level + 1))
        queue.append((right_node, right_value, level + 1))
    return root_node

def print_tree_dict(tree: Dict[str, Any], level: int = 0) -> None:
    """Выводит дерево в виде словаря в удобочитаемом формате."""
    if not tree:
        return
    indent = "  " * level
    print(f"{indent}{{")
    print(f"{indent}  'value': {tree['value']},")
    if tree['left']:
        print(f"{indent}  'left': ")
        print_tree_dict(tree['left'], level + 2)
    else:
        print(f"{indent}  'left': None,")
    if tree['right']:
        print(f"{indent}  'right': ")
        print_tree_dict(tree['right'], level + 2)
    else:
        print(f"{indent}  'right': None")
    print(f"{indent}}}", end=",\n" if level > 0 else "\n")

if __name__ == "__main__":
    """Пример 1: Дерево по умолчанию"""
    print("Пример 1: Дерево по умолчанию (height=4, root=4):")
    tree1 = gen_bin_tree()
    print_tree_dict(tree1)
    """Пример 2: Кастомное дерево"""
    print("\nПример 2: Кастомное дерево (height=3, root=2):")
    tree2 = gen_bin_tree(height=3, root=2)
    print_tree_dict(tree2)
    """Пример 3: С другим правилом генерации"""
    print("\nПример 3: С кастомными функциями:")
    tree3 = gen_bin_tree(
        height=3,
        root=1,
        left_branch=lambda x: x * 2,
        right_branch=lambda x: x * 3
    )
    print_tree_dict(tree3)
    """Пример 4: Представление в виде списка"""
    print("\nПример 4: Дерево в виде списка:")
    tree_list = gen_bin_tree_list(height=3, root=1)
    print(tree_list)
    """Пример 5: Представление в виде namedtuple"""
    print("\nПример 5: Дерево в виде namedtuple (корневое значение):")
    tree_namedtuple = gen_bin_tree_namedtuple(height=3, root=1)
    if tree_namedtuple:
        print(f"Корень: {tree_namedtuple.value}")
        if tree_namedtuple.left:
            print(f"Левый потомок корня: {tree_namedtuple.left.value}")
        if tree_namedtuple.right:
            print(f"Правый потомок корня: {tree_namedtuple.right.value}")