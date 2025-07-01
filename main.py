import json


class Product:
    """
    Класс для представления продукта.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Полностью приватный атрибут цены
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return self.__price * self.quantity + other.__price * other.quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list=None):
        """
        Класс-метод для создания нового продукта
        """
        if products_list is None:
            products_list = []

        # Проверка на дубликаты (доп. задание к заданию 3)
        for product in products_list:
            if product.name.lower() == product_data["name"].lower():
                product.quantity += product_data["quantity"]
                if product_data["price"] > product.__price:  # Полностью приватны атрибут
                    product.__price = product_data["price"]
                return product

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        """Геттер для полностью приватного атрибута цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:  # Доп. задание к заданию 4
            confirmation = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if confirmation.lower() == "y":
                self.__price = new_price
        else:
            self.__price = new_price


class Category:
    """
    Класс для представления категории товаров.
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self.__products)

    def add_product(self, product):
        """Метод для добавления продукта в категорию"""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        """Геттер для списка продуктов"""
        return "\n".join(str(product) for product in self.__products)


class CategoryIterator:
    def __init__(self, products):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration


def load_data_from_json(filename: str) -> list[Category]:
    """
    Загружает данные о категориях и продуктах из JSON-файла.
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            product = Product.new_product(product_data)
            products.append(product)

        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Пример использования (можно оставить как было)
    pass
