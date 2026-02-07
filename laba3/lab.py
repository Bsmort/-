# Построение бинарного дерева
import unittest
from typing import List, Tuple

#параметры по умолчанию
par_height = 4
par_root = 4

#функция вычисления левого потомка
def left_branch(root:int) -> int:
    return root * 4

#функция вычисления правого потомка
def right_branch(root:int) -> int:
    return root + 1

def gen_bin_tree(height:int, root:int) -> dict:
    """
    Создает бинарное дерево рекурсивно и возвращает его в виде словаря.
    
    Аргументы:
        height (int): высота дерева (сколько уровней)
        root (int): значение корневого узла
    
    Возвращает:
        dict: дерево в виде словаря
    """
    # Базовый случай: если высота 1, возвращаем просто корень
    if height == 1:
        return {"root": root}
    
    # Рекурсивно создаем левое и правое поддеревья
    left_leaf = gen_bin_tree(height - 1, left_branch(root))   # левый потомок = root * 2
    right_leaf = gen_bin_tree(height - 1, right_branch(root))  # правый потомок = root + 3
    
    # Возвращаем дерево в виде словаря
    return {
        "root": root,
        "left_leaf": left_leaf,
        "right_leaf": right_leaf
    }

def print_tree(tree, level:int=0):
    """
    Красиво печатает дерево в консоли.
    
    Аргументы:
        tree (dict): дерево для печати
        level (int): текущий уровень (для отступов)
    """
    if not tree:
        return
    
    # Отступ в зависимости от уровня
    indent = "  " * level
    
    # Печатаем текущий узел
    print(f"{indent}├── {tree['root']}")
    
    # Рекурсивно печатаем левое и правое поддеревья
    if "left_leaf" in tree:
        print_tree(tree["left_leaf"], level + 1)
    if "right_leaf" in tree:
        print_tree(tree["right_leaf"], level + 1) 
 
def count_nodes(tree):
    """
    Считает количество узлов в дереве.
    
    Аргументы:
        tree (dict): дерево для подсчета
    
    Возвращает:
        int: количество узлов
    """
    if not tree or "root" not in tree:
        return 0
    
    # Считаем текущий узел + узлы в левом и правом поддеревьях
    total = 1
    if "left_leaf" in tree:
        total += count_nodes(tree["left_leaf"])
    if "right_leaf" in tree:
        total += count_nodes(tree["right_leaf"])
    
    return total        

# Тесты
class TestMath(unittest.TestCase):
    def test_default_tree(self):
        result = gen_bin_tree(par_height, par_root)
        self.assertIn("root", result)
        self.assertEqual(result["root"], 4)

    def test_tree_structure_height_2(self):
        """Тест структуры дерева высотой 2"""
        tree = gen_bin_tree(2, 1)
        
        # Проверяем структуру корня
        self.assertEqual(tree["root"], 1)
        self.assertIn("left_leaf", tree)
        self.assertIn("right_leaf", tree)
        
        # Проверяем левого потомка (1 * 2 = 2)
        left_subtree = tree["left_leaf"]
        self.assertEqual(left_subtree["root"], 4)
        self.assertNotIn("left_leaf", left_subtree)  # Лист, высота 1
        self.assertNotIn("right_leaf", left_subtree)
        
        # Проверяем правого потомка (1 + 3 = 4)
        right_subtree = tree["right_leaf"]
        self.assertEqual(right_subtree["root"], 2)
        self.assertNotIn("left_leaf", right_subtree)  # Лист, высота 1
        self.assertNotIn("right_leaf", right_subtree)
    
    def test_tree_height_3_complex_structure(self):
        """Тест сложного дерева высотой 3"""
        tree = gen_bin_tree(3, 1)
        
        # Проверяем корень
        self.assertEqual(tree["root"], 1)
        
        # Проверяем структуру левого поддерева
        left_subtree = tree["left_leaf"]
        self.assertEqual(left_subtree["root"], 4)  # 1 * 2
        
        # Левый потомок узла 2
        self.assertEqual(left_subtree["left_leaf"]["root"], 16)  # 4 * 4
        self.assertNotIn("left_leaf", left_subtree["left_leaf"])
        self.assertNotIn("right_leaf", left_subtree["left_leaf"])
        
        # Правый потомок узла 2
        self.assertEqual(left_subtree["right_leaf"]["root"], 5)  # 2 + 3
        self.assertNotIn("left_leaf", left_subtree["right_leaf"])
        self.assertNotIn("right_leaf", left_subtree["right_leaf"])
        
        # Проверяем структуру правого поддерева
        right_subtree = tree["right_leaf"]
        self.assertEqual(right_subtree["root"], 2)  # 1 + 1
        
        # Левый потомок узла 4
        self.assertEqual(right_subtree["left_leaf"]["root"], 8)  # 4 * 2
        
        # Правый потомок узла 4
        self.assertEqual(right_subtree["right_leaf"]["root"], 3)  # 
    
    def test_count_nodes_function(self):
        """Тест функции подсчета узлов"""
        # Дерево высотой 1: 1 узел
        tree1 = gen_bin_tree(1, 5)
        self.assertEqual(count_nodes(tree1), 1)
        
        # Дерево высотой 2: 1 корень + 2 листа = 3 узла
        tree2 = gen_bin_tree(2, 5)
        self.assertEqual(count_nodes(tree2), 3)
        
        # Дерево высотой 3: полное бинарное дерево высотой 3 = 7 узлов
        tree3 = gen_bin_tree(3, 5)
        self.assertEqual(count_nodes(tree3), 7)
        
        # Дерево высотой 4: полное бинарное дерево высотой 4 = 15 узлов
        tree4 = gen_bin_tree(4, 5)
        self.assertEqual(count_nodes(tree4), 15)
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Высота 0 или отрицательная (ожидается падение или пустое дерево)
        # В текущей реализации при height=1 возвращается только корень
        tree = gen_bin_tree(1, 10)
        self.assertEqual(tree["root"], 10)
        self.assertNotIn("left_leaf", tree)
        self.assertNotIn("right_leaf", tree)
        
        # Большое значение корня
        tree_large = gen_bin_tree(2, 1000)
        self.assertEqual(tree_large["root"], 1000)
        self.assertEqual(tree_large["left_leaf"]["root"], 4000)  # 1000 * 4
        self.assertEqual(tree_large["right_leaf"]["root"], 1001)  # 1000 + 1

# Запуск тестов
if __name__ == '__main__':
    print("Бинарное дерево (вариант 1)")
    print("=" * 30)
    unittest.main(argv=[''], verbosity=2, exit=False)