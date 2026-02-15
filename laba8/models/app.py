class App:
    def __init__(self, name: str, version: str, author: Author):
        self._name = None
        self._version = None
        self._author = None
        # Инициализация через сеттеры
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название приложения должно быть строкой.")
        if not value.strip():
            raise ValueError("Название приложения не может быть пустым.")
        self._name = value.strip()

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Версия приложения должна быть строкой.")
        if not value.strip():
            raise ValueError("Версия приложения не может быть пустой.")
        self._version = value.strip()

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, value: Author):
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть экземпляром класса Author.")
        self._author = value

    def __repr__(self) -> str:
        return (f"<App(name='{self.name}', "
                f"version='{self.version}', "
                f"author={self.author})>")