import hashlib
import random
import re


class IdCounter:
    def __init__(self):
        self.counter = 0

    def get_new_id(self):
        self.counter += 1
        return self.counter


class Password:
    @staticmethod
    def get(password):
        if not isinstance(password, str):
            raise TypeError("Пароль должен быть строкового типа")
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
            raise ValueError("Длина пароля должна быть больше, чем 8 символов и содержать как буквы, так и цифры")
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check(password, hashed_password):
        return Password.get(password) == hashed_password


class Product:
    id_counter = IdCounter()

    def __init__(self, name, price, rating):
        self._id = self.id_counter.get_new_id()
        self._name = name
        self._price = price
        self._rating = rating

    def __str__(self):
        return f"{self._id}_{self._name}"

    def __repr__(self):
        return f"Product(id={self.id}, name='{self._name}')"


class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)


class User:
    id_counter = IdCounter()

    def __init__(self, username, password):
        self._id = self.id_counter.get_new_id()
        self._username = username
        self._password = password
        self.username = username
        self._password_hash = Password.get(password)
        self._cart = Cart()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя пользователя должно быть в строковом формате")
        if len(value) < 3:
            raise ValueError("Имя пользователя должно быть длиннее трех символов")
        self._username = value

    @property
    def cart(self):
        return self._cart

    def __str__(self):
        return f"User(id={self._id}, username='{self._username}, password='password1')"

    def __repr__(self):
        return self.__str__()


class Store:
    def __init__(self):
        self.users = []

    def authenticate(self):
        username = input("Введите имя пользователя:")
        password = input("Введите пароль:")
        for user in self.users:
            if user.username == username and Password.check(password, user._password_hash):
                print("Данные верны. Аутентификация успешна")
                return user
                break
            print("Данные неверны. Аутентификация не пройдена")
            return None

    def add_random_product_to_cart(self, user):
        product = self.generate_random_product()
        user.cart.add_product(product)
        print(f"Добавлен {product} в корзину")

    def generate_random_product(self):
        random_name = random.choice(["Фен", "Холодильник", "Стиральная машина", "Бойлер"])
        random_price = round(random.uniform(100, 1000), 2)
        random_rating = round(random.uniform(1, 5), 2)
        return Product(random_name, random_price, random_rating)

    def view_cart(self, user):
        print("Наполнение корзины")
        for product in user.cart.products:
            print(product)


if __name__ == '__main__':
    store = Store()
    user1 = User("Алена", "123password")
    user2 = User("Никита", "strongPassw289")
    store.users.append(user1)
    store.users.append(user2)

    authenticated_user = store.authenticate()
    if authenticated_user:
        store.add_random_product_to_cart(authenticated_user)
        store.add_random_product_to_cart(authenticated_user)
        store.view_cart(authenticated_user)
