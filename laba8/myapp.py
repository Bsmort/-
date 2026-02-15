from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies

# Инициализация Jinja2 (один раз)
env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape()
)

# Загрузка шаблонов
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")

# Данные приложения (можно заменить на БД)
main_author = Author("Иван Петров", "ПИ-123")
app = App("CurrencyTracker", "1.0", main_author)
users = [User(1, "Алексей"), User(2, "Мария")]
user_currencies = [UserCurrency(1, 1, 840), UserCurrency(2, 2, 978)]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)

        if path == "/":
            self.show_index()
        elif path == "/users":
            self.show_users()
        elif path == "/user" and "id" in query:
            self.show_user(int(query["id"][0]))
        elif path == "/currencies":
            self.show_currencies()
        elif path == "/author":
            self.show_author()
        else:
            self.send_error(404, "Not Found")

    def show_index(self):
        html = template_index.render(
            app_name=app.name,
            version=app.version,
            author_name=main_author.name,
            group=main_author.group,
            navigation=[{"caption": "Главная", "href": "/"}]
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def show_users(self):
        html = template_users.render(users=users)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def show_user(self, user_id: int):
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            self.send_error(404, "User not found")
            return

        # Получаем подписки пользователя
        subscriptions = [
            (uc, next((c for c in get_currencies() if c.id == uc.currency_id), None))
            for uc in user_currencies if uc.user_id == user_id
        ]

        html = template_currencies.render(user=user, subscriptions=subscriptions)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def show_currencies(self):
        currencies = get_currencies()
        html = template_currencies.render(currencies=currencies)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def show_author(self):
        html = f"""
        <h1>Автор</h1>
        <p>Имя: {main_author.name}</p>
        <p>Группа: {main_author.group}</p>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")