class Currency:
    def __init__(self, id: int, num_code: str, char_code: str,
                 name: str, value: float, nominal: int):
        self._id = None
        self._num_code = None
        self._char_code = None
        self._name = None
        self._value = None
        self._nominal = None
        # Инициализация через сеттеры
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID валюты должен быть целым числом.")
        if value <= 0:
            raise ValueError("ID валюты должен быть положительным числом.")
        self._id = value

    @property
    def num_code(self) -> str:
        return self._num_code

    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Цифровой код валюты должен быть строкой.")
        if not value.isdigit():
            raise ValueError("Цифровой код валюты должен содержать только цифры.")
        if len(value) < 1 or len(value) > 4:  # примерная длина
            raise ValueError("Цифровой код валюты должен быть от 1 до 4 цифр.")
        self._num_code = value

    @property
    def char_code(self) -> str:
        return self._char_code

    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Символьный код валюты должен быть строкой.")
        if not value.isalpha():
            raise ValueError("Символьный код валюты должен содержать только буквы.")
        if len(value) != 3:
            raise ValueError("Символьный код валюты должен состоять из 3 букв (например, USD).")
        self._char_code = value.upper()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название валюты должно быть строкой.")
        if not value.strip():
            raise ValueError("Название валюты не может быть пустым.")
        self._name = value.strip()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Курс валюты должен быть числом (int или float).")
        if value < 0:
            raise ValueError("Курс валюты не может быть отрицательным.")
        self._value = float(value)

    @property
    def nominal(self) -> int:
        return self._nominal

    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Номинал должен быть целым числом.")
        if value <= 0:
            raise ValueError("Номинал должен быть положительным числом.")
        self._nominal = value

    def __repr__(self) -> str:
        return (f"<Currency(id={self.id}, "
                f!num_code='{self.num_code}', "
                f!char_code='{self.char_code}', "
                f!name='{self.name}', "
                f!value={self.value}, "
                f!nominal={self.nominal})>")