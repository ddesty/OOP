import pytest
from main import Category, Product, load_data_from_json  # Добавили импорт функции


@pytest.fixture
def sample_product() -> Product:
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category("Test Category", "Test Description", [sample_product])


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
    initial_count = len(sample_category.products.split('\n'))
    new_product = Product("New Product", "Desc", 50.0, 10)
    sample_category.add_product(new_product)
    assert len(sample_category.products.split('\n')) == initial_count + 1
    assert "New Product, 50.0 руб. Остаток: 10 шт." in sample_category.products


def test_add_invalid_product(sample_category: Category) -> None:
    with pytest.raises(TypeError):
        sample_category.add_product("not a product")


def test_product_price_setter(sample_product: Product, monkeypatch) -> None:
    sample_product.price = 150.0
    assert sample_product.price == 150.0

    # Тест на отрицательную цену
    sample_product.price = -10
    assert sample_product.price == 150.0  # Цена не должна измениться

    # Тест на понижение цены с mock вводом 'y'
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    sample_product.price = 120.0
    assert sample_product.price == 120.0

    # Тест на понижение цены с mock вводом 'n'
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    sample_product.price = 100.0
    assert sample_product.price == 120.0  # Цена не должна измениться


def test_fully_private_price():
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
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 5
    }
    product = Product.new_product(product_data)
    assert isinstance(product, Product)
    assert product.name == "Test Product"


def test_new_product_duplicate() -> None:
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 5
    }
    existing_products = [Product("Test Product", "Old Desc", 90.0, 3)]
    product = Product.new_product(product_data, existing_products)
    assert product.quantity == 8  # 3 + 5
    assert product.price == 100.0  # Более высокая цена


def test_load_data_from_json(tmp_path):
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
    test_file.write_text(json_data, encoding='utf-8')

    # Тестируем загрузку
    categories = load_data_from_json(str(test_file))
    assert len(categories) == 1
    assert categories[0].name == "Test Category"
    assert "Test Product, 100.0 руб. Остаток: 5 шт." in categories[0].products
