from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from main import BaseProduct
from main import Category
from main import LawnGrass
from main import Product
from main import Smartphone
from main import load_data_from_json


@pytest.fixture
def sample_product() -> Product:
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category("Test Category", "Test Description", [sample_product])


@pytest.fixture
def sample_smartphone() -> Smartphone:
    return Smartphone("iPhone 15", "Flagship smartphone", 100000.0, 10, 3.5, "15 Pro", 256, "Space Gray")


@pytest.fixture
def sample_lawn_grass() -> LawnGrass:
    return LawnGrass("Premium Grass", "High quality lawn grass", 500.0, 100, "Russia", 14, "Green")


def test_product_init(sample_product: Product) -> None:
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 100.0
    assert sample_product.quantity == 5


def test_category_init(sample_category: Category, sample_product: Product) -> None:
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Description"
    assert "Test Product, 100.0 руб. Остаток: 5 шт." in sample_category.products


def test_category_count() -> None:
    initial_count = Category.category_count
    Category("New Category", "Description", [])
    assert Category.category_count == initial_count + 1


def test_product_count(sample_product: Product) -> None:
    initial_count = Category.product_count
    Category("New Category", "Description", [sample_product, sample_product])
    assert Category.product_count == initial_count + 2


def test_add_product(sample_category: Category) -> None:
    initial_count = len(sample_category.products.split("\n"))
    new_product = Product("New Product", "Desc", 50.0, 10)
    sample_category.add_product(new_product)
    assert len(sample_category.products.split("\n")) == initial_count + 1
    assert "New Product, 50.0 руб. Остаток: 10 шт." in sample_category.products


def test_product_price_setter(sample_product: Product, monkeypatch: MonkeyPatch) -> None:
    sample_product.price = 150.0
    assert sample_product.price == 150.0

    # Тест на отрицательную цену
    sample_product.price = -10
    assert sample_product.price == 150.0  # Цена не должна измениться

    # Тест на понижение цены с mock вводом 'y'
    monkeypatch.setattr("builtins.input", lambda _: "y")
    sample_product.price = 120.0
    assert sample_product.price == 120.0

    # Тест на понижение цены с mock вводом 'n'
    monkeypatch.setattr("builtins.input", lambda _: "n")
    sample_product.price = 100.0
    assert sample_product.price == 120.0  # Цена не должна измениться


def test_fully_private_price() -> None:
    """Тест на полностью приватный атрибут цены"""
    product = Product("Test", "Desc", 100.0, 5)

    # Проверяем, что атрибут действительно приватный
    with pytest.raises(AttributeError):
        product.__price

    # Проверяем работу через геттер/сеттер
    assert product.price == 100.0
    product.price = 150.0
    assert product.price == 150.0


def test_new_product_classmethod() -> None:
    product_data = {"name": "Test Product", "description": "Test Description", "price": 100.0, "quantity": 5}
    product = Product.new_product(product_data)
    assert isinstance(product, Product)
    assert product.name == "Test Product"


def test_new_product_duplicate() -> None:
    product_data = {"name": "Test Product", "description": "Test Description", "price": 100.0, "quantity": 5}
    existing_products = [Product("Test Product", "Old Desc", 90.0, 3)]
    product = Product.new_product(product_data, existing_products)
    assert product.quantity == 8  # 3 + 5
    assert product.price == 100.0  # Более высокая цена


def test_load_data_from_json(tmp_path: Path) -> None:
    # Создаем временный JSON файл
    json_data = """
    [
      {
        "name": "Test Category",
        "description": "Test Description",
        "products": [
          {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100.0,
            "quantity": 5
          }
        ]
      }
    ]
    """
    test_file = tmp_path / "test_products.json"
    test_file.write_text(json_data, encoding="utf-8")

    # Тестируем загрузку
    categories = load_data_from_json(str(test_file))
    assert len(categories) == 1
    assert categories[0].name == "Test Category"
    assert "Test Product, 100.0 руб. Остаток: 5 шт." in categories[0].products


# Новые тесты для 14.3 (добавляем в конец файла)
def test_product_str(sample_product: Product) -> None:
    assert str(sample_product) == "Test Product, 100.0 руб. Остаток: 5 шт."


def test_category_str(sample_category: Category) -> None:
    assert str(sample_category) == "Test Category, количество продуктов: 5 шт."


def test_product_addition(sample_product: Product) -> None:
    product2 = Product("Product 2", "Desc", 200.0, 3)
    assert sample_product + product2 == 100.0 * 5 + 200.0 * 3


def test_product_addition_invalid(sample_product: Product) -> None:
    with pytest.raises(TypeError):
        sample_product + "not a product"  # type: ignore[operator]


def test_category_iterator(sample_category: Category) -> None:
    products = list(sample_category)
    assert len(products) == 1
    assert products[0].name == "Test Product"


def test_category_iterator_empty() -> None:
    empty_category = Category("Empty", "Empty", [])
    products = list(empty_category)
    assert len(products) == 0


# Новые тесты для 16.1
def test_smartphone_init(sample_smartphone: Smartphone) -> None:
    assert sample_smartphone.name == "iPhone 15"
    assert sample_smartphone.efficiency == 3.5
    assert sample_smartphone.model == "15 Pro"
    assert sample_smartphone.memory == 256
    assert sample_smartphone.color == "Space Gray"


def test_lawn_grass_init(sample_lawn_grass: LawnGrass) -> None:
    assert sample_lawn_grass.name == "Premium Grass"
    assert sample_lawn_grass.country == "Russia"
    assert sample_lawn_grass.germination_period == 14
    assert sample_lawn_grass.color == "Green"


def test_product_addition_different_types(sample_smartphone: Smartphone, sample_lawn_grass: LawnGrass) -> None:
    with pytest.raises(TypeError):
        sample_smartphone + sample_lawn_grass


def test_add_valid_product_types(
    sample_category: Category, sample_smartphone: Smartphone, sample_lawn_grass: LawnGrass
) -> None:
    initial_count = len(sample_category.products.split("\n"))
    sample_category.add_product(sample_smartphone)
    sample_category.add_product(sample_lawn_grass)
    assert len(sample_category.products.split("\n")) == initial_count + 2


def test_inheritance_relations() -> None:
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)
    smartphone = Smartphone("Test", "Test", 100.0, 1, 1.0, "X", 128, "Black")
    assert isinstance(smartphone, Product)


# Тесты для 16.2
def test_base_product_abstract_methods() -> None:
    with pytest.raises(TypeError):
        BaseProduct("Test", "Desc", 100.0, 5)  # type: ignore[abstract]


def test_create_log_mixin_output(capsys: pytest.CaptureFixture[str]) -> None:
    Product("LogTest", "Desc", 100.0, 2)
    captured = capsys.readouterr()
    assert "Создан объект класса Product с параметрами" in captured.out
    assert "LogTest" in captured.out


# Тесты для новых функций 17.1
def test_zero_quantity_product() -> None:
    """Тест на создание товара с нулевым количеством"""
    with pytest.raises(ValueError):
        Product("Invalid", "Desc", 100.0, 0)


def test_category_middle_price(sample_category: Category, sample_product: Product) -> None:
    """Тест расчета средней цены"""
    assert sample_category.middle_price() == 100.0

    empty_category = Category("Empty", "Desc", [])
    assert empty_category.middle_price() == 0


def test_add_product_with_zero_quantity(sample_category: Category, capsys: pytest.CaptureFixture[str]) -> None:
    """Тест добавления товара с нулевым количеством"""
    initial_count = len(list(sample_category))

    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Zero", "Desc", 100.0, 0)
        # Проверяем, что категория не изменилась
    assert len(list(sample_category)) == initial_count
