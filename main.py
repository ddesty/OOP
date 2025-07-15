import json
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List


# Дополнительное задание: Пользовательское исключение
class ZeroQuantityError(ValueError):
    """Исключение для товаров с нулевым количеством"""

    pass


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов
    """

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.quantity = quantity
        self.__price = price

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        pass


class CreateLogMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {args}")
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        name = getattr(self, "name", "N/A")
        description = getattr(self, "description", "N/A")
        price = getattr(self, "price", "N/A")
        quantity = getattr(self, "quantity", "N/A")
        return f"{self.__class__.__name__}({name}, {description}, {price}, {quantity})"


class Product(CreateLogMixin, BaseProduct):
    """
    Класс для представления продукта.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        # Задание 1: Проверка нулевого количества
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price  # Полностью приватный атрибут цены
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, self.__class__):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.__price * self.quantity + other.__price * other.quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, Any], products_list: List["Product"] | None = None) -> "Product":
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
    def price(self) -> float:
        """Геттер для полностью приватного атрибута цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:  # Доп. задание к заданию 4
            confirmation = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if confirmation.lower() == "y":
                self.__price = new_price
        else:
            self.__price = new_price


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator[Product]:
        return CategoryIterator(self.__products)

    def middle_price(self) -> float:
        """Задание 2: Метод для расчета средней цены товаров"""
        try:
            total_price = sum(product.price for product in self.__products)
            return float(total_price / len(self.__products))
        except ZeroDivisionError:
            return 0.0

    def add_product(self, product: Product) -> None:
        """Доп. задание: Обновленный метод добавления товара с обработкой исключений"""
        try:
            if product.quantity == 0:
                raise ZeroQuantityError(f"Товар '{product.name}' не может быть добавлен с нулевым количеством")

            if isinstance(product, Product):
                self.__products.append(product)
                Category.product_count += 1
                print(f"Товар '{product.name}' успешно добавлен")
            else:
                raise TypeError("Можно добавлять только объекты класса Product")

        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
        except TypeError as e:
            print(f"Ошибка: {e}")
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> str:
        """Геттер для списка продуктов"""
        return "\n".join(str(product) for product in self.__products)


class CategoryIterator:
    def __init__(self, products: List[Product]) -> None:
        self.products = products
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
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
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError:
        print("Возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
