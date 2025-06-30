import pytest

from main import Category
from main import Product


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
    assert len(sample_category.products) == 1
    assert sample_category.products[0] == sample_product


def test_category_count() -> None:
    initial_count = Category.category_count
    Category("New Category", "Description", [])
    assert Category.category_count == initial_count + 1


def test_product_count(sample_product: Product) -> None:
    initial_count = Category.product_count
    Category("New Category", "Description", [sample_product, sample_product])
    assert Category.product_count == initial_count + 2
