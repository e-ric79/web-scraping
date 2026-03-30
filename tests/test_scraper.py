from src.scraperapi_Client import (
    clean_product_name,
    normalize_product,
    extract_search_results,
)


def test_clean_product_name_removes_dash():
    result = clean_product_name("Samsung Galaxy S24 - 256GB")
    assert "Samsung Galaxy S24" == result


def test_clean_product_name_removes_special_chars():
    result = clean_product_name('Lenovo ThinkPad 14" Laptop')
    assert '"' not in result


def test_clean_product_name_max_5_words():
    result = clean_product_name("One Two Three Four Five Six Seven")
    assert len(result.split()) <= 5


def test_normalize_product_returns_dict():
    fake_content = {
        "name": "Test Product",
        "pricing": "$99.99",
        "average_rating": 4.5,
        "brand": "TestBrand",
        "images": [],
    }
    result = normalize_product(fake_content)
    assert isinstance(result, dict)
    assert result["title"] == "Test Product"
    assert result["price"] == "$99.99"


def test_extract_search_results_empty():
    result = extract_search_results({})
    assert result == []


def test_extract_search_results_with_results():
    fake_content = {
        "results": [
            {"asin": "B001", "name": "Product 1"},
            {"asin": "B002", "name": "Product 2"},
        ]
    }
    result = extract_search_results(fake_content)
    assert len(result) == 2
