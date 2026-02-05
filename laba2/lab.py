import unittest
from typing import List, Tuple

# Функция медленного перебора (инкремента)
def guess_number(target, numbers):
    attempts = 0
    for num in numbers:
        attempts += 1
        if num == target:
            return target, attempts
    return None, attempts  # Возвращаем None, если число не найдено

def helper() -> Tuple[int, List[int]]:    
    # Вспомогательная функция для получения входных данных от пользователя.
    
    # Получаем диапазон
    while True:
        try:
            start = int(input("Введите начало диапазона: "))
            end = int(input("Введите конец диапазона: "))
            if start > end:
                print("Ошибка: начало диапазона не может быть больше конца!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целые числа!")

    # Создаем список чисел
    numbers = list(range(start, end + 1))
    print(f"Создан список из {len(numbers)} чисел: от {start} до {end}")
    
    # Получаем число для угадывания
    while True:
        try:
            target = int(input(f"Введите число для угадывания (от {start} до {end}): "))
            
            if target not in numbers:
                print(f"Ошибка: число должно быть в диапазоне от {start} до {end}!")
                continue
                
            break
        except ValueError:
            print("Ошибка: введите целое число!")

    return target, numbers

# Тесты
class TestMath(unittest.TestCase):
    """Тесты для функций угадывания чисел."""

    def test_linear_search_small(self):
        """Тест медленного перебора"""
        begin_range = 1
        end_range = 10
        numbers = list(range(begin_range, end_range + 1))
        target = 7
        result, attempts = guess_number(target, numbers)  # Используем локальную переменную numbers
        self.assertEqual(result, target)  # Проверяем, что найденное число равно целевому
        self.assertEqual(attempts, 7)  # Дополнительная проверка: должно быть 7 попыток

    def test_number_not_found(self):
        """Тест случая, когда число не найдено."""
        begin_range = 1
        end_range = 10
        numbers = list(range(begin_range, end_range + 1))
        target = 11
        result, attempts = guess_number(target, numbers)
        self.assertIsNone(result)  # Проверяем, что результат None
        self.assertEqual(attempts, 10)  # Все 5 чисел были проверены

# Запуск тестов
if __name__ == '__main__':
    # helper() - для ручного тестирования
    #result, attempts = helper();
    unittest.main(argv=[''], verbosity=2, exit=False)