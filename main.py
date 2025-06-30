import json


class Product:
    """
    Класс для представления продукта.

    Атрибуты:
        name (str): Название продукта
        description (str): Описание продукта
        price (float): Цена продукта
        quantity (int): Количество доступных единиц
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
        name (str): Название категории
        description (str): Описание категории
        products (list): Список продуктов в категории

    Атрибуты класса:
        category_count (int): Счетчик категорий
        product_count (int): Счетчик продуктов
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def load_data_from_json(filename: str) -> list[Category]:
    """
    Загружает данные о категориях и продуктах из JSON-файла.

    Аргументы:
        filename (str): Путь к JSON-файлу

    Возвращает:
        list[Category]: Список объектов Category
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products.append(product)

        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Пример создания объектов вручную
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("Информация о продуктах:")
    print(f"{product1.name}: {product1.price} руб. (Остаток: {product1.quantity} шт.)")
    print(f"{product2.name}: {product2.price} руб. (Остаток: {product2.quantity} шт.)")
    print(f"{product3.name}: {product3.price} руб. (Остаток: {product3.quantity} шт.)")

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print("\nИнформация о категории:")
    print(f"Название: {category1.name}")
    print(f"Описание: {category1.description}")
    print(f"Количество продуктов: {len(category1.products)}")

    # Пример загрузки данных из JSON
    print("\nЗагрузка данных из JSON:")
    try:
        categories = load_data_from_json("products.json")
        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Описание: {category.description}")
            for product in category.products:
                print(f"  - {product.name}: {product.price} руб. (Остаток: {product.quantity} шт.)")

        print(f"\nОбщее количество категорий: {Category.category_count}")
        print(f"Общее количество продуктов: {Category.product_count}")
    except FileNotFoundError:
        print("Файл products.json не найден!")
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON-файла!")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
