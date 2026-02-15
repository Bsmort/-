class Author:
    def __init__(self, name: str, group: str):
        self._name = None
        self._group = None
        # Инициализация через сеттеры (с валидацией)
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Имя автора должно быть строкой.")
        if not value.strip():
            raise ValueError("Имя автора не может быть пустым.")
        self._name = value.strip()

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой.")
        if not value.strip():
            raise ValueError("Название группы не может быть пустым.")
        self._group = value.strip()

    def __repr__(self) -> str:
        return f"<Author(name='{self.name}', group='{self.group}')>"