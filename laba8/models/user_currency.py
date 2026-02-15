class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: int):
        self._id = None
        self._user_id = None
        self._currency_id = None
        # Инициализация через сеттеры
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID связи должен быть целым числом.")
        if value <= 0:
            raise ValueError("ID связи должен быть положительным