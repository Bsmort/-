import sys
import io
import logging
import requests
import json
import math
import unittest
from functools import wraps
from datetime import datetime
from typing import Dict, List


""" 1. Реализовать декоратор logger """
def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция (если используется без скобок)
        handle: Цель для логирования (sys.stdout, io.StringIO, logging.Logger)
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal handle
            """Формируем строку с аргументами"""
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            """Логирование начала выполнения"""
            start_msg = f"[{timestamp}] INFO: Function '{f.__name__}' called with args: ({signature})\n"
            if isinstance(handle, logging.Logger):
                handle.info(f"Function '{f.__name__}' called with args: ({signature})")
            else:
                handle.write(start_msg)
                if hasattr(handle, 'flush'):
                    handle.flush()
            try:
                """Выполнение функции"""
                result = f(*args, **kwargs)
                """Логирование успешного завершения"""
                end_msg = f"[{timestamp}] INFO: Function '{f.__name__}' returned: {result!r}\n"
                if isinstance(handle, logging.Logger):
                    handle.info(f"Function '{f.__name__}' returned: {result!r}")
                else:
                    handle.write(end_msg)
                    if hasattr(handle, 'flush'):
                        handle.flush()
                return result
            except Exception as e:
                """Логирование ошибки"""
                error_msg = f"[{timestamp}] ERROR: Function '{f.__name__}' raised {type(e).__name__}: {str(e)}\n"
                if isinstance(handle, logging.Logger):
                    handle.error(f"Function '{f.__name__}' raised {type(e).__name__}: {str(e)}")
                else:
                    handle.write(error_msg)
                    if hasattr(handle, 'flush'):
                        handle.flush()
                """Повторно выбрасываем исключение"""
                raise
        return wrapper
    """Если декоратор используется без скобок: @logger"""
    if func is None:
        return decorator
    """Если декоратор используется без скобок: @logger"""
    return decorator(func)


""" Реализовать функцию get_currencies """
def get_currencies(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    """ Получает курсы валют с API ЦБ РФ. """

    """
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ

    Returns:
        Словарь с курсами валют

    Raises:
        ConnectionError: Если API недоступен
        ValueError: Если некорректный JSON
        KeyError: Если отсутствует ключ 'Valute' или валюта
        TypeError: Если курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"API недоступен: {str(e)}")
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON: {str(e)}")
    """Проверяем наличие ключа 'Valute'"""
    if 'Valute' not in data:
        raise KeyError("В ответе API отсутствует ключ 'Valute'")
    valutes = data['Valute']
    result = {}
    for code in currency_codes:
        if code not in valutes:
            raise KeyError(f"Валюта '{code}' отсутствует в данных API")
        try:
            """ Получаем значение курса """
            currency_data = valutes[code]
            value = currency_data['Value']
            """ Проверяем тип """
            if not isinstance(value, (int, float)):
                raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")
            result[code] = value
        except KeyError:
            raise KeyError(f"В данных валюты '{code}' отсутствует ключ 'Value'")
    return result


""" 3. Обернуть функцию декоратором """
@logger(handle = sys.stdout)
def get_currencies_decorated(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, float]:
    return get_currencies(currency_codes, url)

""" 5. Демонстрационный пример """
logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)
def solve_quadratic(a, b, c):
    logging.info(f"Solving equation: {a}x^2 + {b}x + {c} = 0")
    """Ошибка типов"""
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            logging.critical(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Coefficient '{name}' must be numeric")
    """Ошибка: a == 0"""
    if a == 0:
        logging.error("Coefficient 'a' cannot be zero")
        raise ValueError("a cannot be zero")
    d = b*b - 4*a*c
    logging.debug(f"Discriminant: {d}")
    if d < 0:
        logging.warning("Discriminant < 0: no real roots")
        return None
    if d == 0:
        x = -b / (2*a)
        logging.info("One real root")
        return (x,)
    root1 = (-b + math.sqrt(d)) / (2*a)
    root2 = (-b - math.sqrt(d)) / (2*a)
    logging.info("Two real roots computed")
    return root1, root2

# Демонстрационная функция для квадратного уравнения с логированием
@logger
def demo_solve_quadratic(a: float, b: float, c: float) -> None:
    """
    Демонстрирует решение квадратного уравнения с логированием.
    
    Args:
        a: Коэффициент при x²
        b: Коэффициент при x
        c: Свободный член
    """
    result = solve_quadratic(a, b, c)
    if result is None:
        print("Уравнение не имеет действительных корней")
    elif isinstance(result, tuple):
        #print(f"Корни уравнения: x1 = {result[0]}, x2 = {result[1]}")
        if len(result) == 2:
            print(f"Корни уравнения: x1 = {result[0]}, x2 = {result[1]}")
        elif len(result) == 1:
            print(f"Корень уравнения: x = {result[0]}")
    else:
        print(f"Корень уравнения: x = {result}")

class TestGetCurrencies(unittest.TestCase):
    """Тесты для функции get_currencies."""
    def test_successful_request(self):
        """Тест успешного получения курсов валют."""
        # Используем только USD, так как он гарантированно есть в ответе
        result = get_currencies(['USD'])
        self.assertIsInstance(result, dict)
        self.assertIn('USD', result)
        self.assertIsInstance(result['USD'], float)
        self.assertGreater(result['USD'], 0)
    def test_invalid_currency(self):
        """Тест запроса несуществующей валюты."""
        with self.assertRaises(KeyError) as context:
            get_currencies(['XXX'])
        self.assertIn('не найдена', str(context.exception))
    def test_connection_error(self):
        """Тест ошибки подключения к API."""
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'], url="https://invalid-url-cbr.ru")
    def test_invalid_json(self):
        """Тест обработки некорректного JSON."""
        with self.assertRaises(ValueError):
            get_currencies(['USD'], url="некорректныйJSON")
    def test_missing_valute_key(self):
        """Тест отсутствия ключа 'Valute' в ответе."""
        # Создаём подмену для тестирования
        def mock_urlopen(*args, **kwargs):
            class MockResponse:
                def read(self):
                    return b'{"foo": "bar"}'
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
            return MockResponse()
        original_urlopen = request.urlopen
        try:
            request.urlopen = mock_urlopen
            with self.assertRaises(KeyError) as context:
                get_currencies(['USD'])
            self.assertIn('отсутствует ключ', str(context.exception))
        finally:
            request.urlopen = original_urlopen

class TestLoggerDecorator(unittest.TestCase):
    """Тесты для декоратора logger."""
    def setUp(self):
        """Настройка тестового окружения."""
        self.stream = io.StringIO()
    def test_successful_execution_logging(self):
        """Тест логирования при успешном выполнении."""
        @logger(handle=self.stream)
        def add(a, b):
            return a + b
        result = add(2, 3)
        self.assertEqual(result, 5)
        logs = self.stream.getvalue()
        self.assertIn("INFO: Вызов функции: add(2, 3)", logs)
        self.assertIn("INFO: Функция add успешно завершена. Результат: 5", logs)
    def test_error_execution_logging(self):
        """Тест логирования при возникновении ошибки."""
        @logger(handle=self.stream)
        def divide(a, b):
            return a / b
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)
        logs = self.stream.getvalue()
        self.assertIn("ERROR: divide вызвала исключение ZeroDivisionError", logs)
        self.assertIn("division by zero", logs)
    def test_logger_with_logging_module(self):
        """Тест логирования через модуль logging."""
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        test_logger = logging.getLogger("test_logger")
        test_logger.setLevel(logging.INFO)
        test_logger.addHandler(handler)
        @logger(handle=test_logger)
        def multiply(a, b):
            return a * b
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        logs = log_stream.getvalue()
        self.assertIn("INFO: Вызов функции: multiply(4, 5)", logs)
        self.assertIn("INFO: Функция multiply успешно завершена. Результат: 20", logs)
    def test_preserve_function_metadata(self):
        """Тест сохранения метаданных функции."""
        @logger
        def test_func():
            """Test documentation."""
            pass
        self.assertEqual(test_func.__name__, "test_func")
        self.assertEqual(test_func.__doc__, "Test documentation.")

    def test_logging_with_args_and_kwargs(self):
        """Тест логирования различных типов аргументов."""
        @logger(handle=self.stream)
        def complex_func(a, b=10, *args, **kwargs):
            return a + b
        result = complex_func(5, 20, 30, extra="test")
        self.assertEqual(result, 25)
        logs = self.stream.getvalue()
        self.assertIn("Вызов функции: complex_func(5, 30, b=20, extra='test')", logs)


class TestStreamWrite(unittest.TestCase):
    """
    Тест для проверки логирования ошибок API через StringIO.
    Из задания: пример с невалидным URL.
    """
    def setUp(self):
        """Настройка тестового окружения."""
        self.stream = io.StringIO()
        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")
        self.wrapped = wrapped
    def test_logging_error(self):
        """Тест логирования ошибки подключения к API."""
        with self.assertRaises(ConnectionError):
            self.wrapped()
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
        self.assertIn("API ЦБ РФ недоступен", logs)


class TestQuadraticEquation(unittest.TestCase):
    """Тесты для решения квадратного уравнения."""
    def test_two_roots(self):
        """Тест с двумя корнями."""
        result = solve_quadratic(1, -5, 6)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (3.0, 2.0))
    def test_one_root(self):
        """Тест с одним корнем."""
        result = solve_quadratic(1, -4, 4)
        self.assertEqual(result, 2.0)
    def test_no_roots(self):
        """Тест без действительных корней."""
        result = solve_quadratic(1, 2, 5)
        self.assertIsNone(result)
    def test_linear_equation(self):
        """Тест линейного уравнения (a=0)."""
        result = solve_quadratic(0, 2, -6)
        self.assertEqual(result, 3.0)
    def test_invalid_input(self):
        """Тест некорректных входных данных."""
        with self.assertRaises(ValueError):
            solve_quadratic("abc", 2, 3)
    def test_infinite_solutions(self):
        """Тест бесконечного количества решений."""
        with self.assertRaises(ZeroDivisionError):
            solve_quadratic(0, 0, 5)

# Пример использования с разными вариантами логирования
def main():
    # 1. Логирование в stdout
    print("\n1. Логирование в stdout:")
    result = get_currencies_decorated(['USD', 'EUR'])
    print(f"Результат: {result}")
    # 2. Логирование в StringIO
    print("\n2. Логирование в StringIO:")
    stream = io.StringIO()
    @logger(handle = stream)
    def multiply(x, y):
        return x * y
    multiply(5, 3)
    print(f"Логи из StringIO:\n{stream.getvalue()}")

    """ 5. Демонстрация demo_solve_quadrati """
    """ Квадратное уравнение с двумя корнями """ 
    print("\n1. Квадратное уравнение с двумя корнями:")
    demo_solve_quadratic(1, -5, 6)
    """ Уравнение с одним корнем """ 
    print("\n2. Уравнение с одним корнем:")
    demo_solve_quadratic(1, -4, 4)
    """ Уравнение без корней """ 
    print("\n3. Уравнение без корней:")
    demo_solve_quadratic(1, 2, 5)
    
    """ Запуск тестов """
    unittest.main(argv=[''], verbosity=2, exit=False)

main()