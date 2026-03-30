import os
import pytest
from src.db import Database

TEST_DB_PATH = "test_data.json"

@pytest.fixture
def db():
    # Clean up before test in case previous run left the file
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    database = Database(db_path=TEST_DB_PATH)
    yield database
    
    # ✅ Close TinyDB before deleting on Windows
    database.db.close()
    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_insert_product(db):
    product = {"asin": "B001TEST", "title": "Test Product", "price": "$99"}
    db.insert_product(product)
    result = db.get_product("B001TEST")
    assert result is not None
    assert result["asin"] == "B001TEST"

def test_get_all_products(db):
    db.insert_product({"asin": "B001", "title": "Product 1"})
    db.insert_product({"asin": "B002", "title": "Product 2"})
    results = db.get_all_products()
    assert len(results) == 2  # ✅ fresh db each time

def test_no_duplicate_asins(db):
    db.insert_product({"asin": "B001", "title": "Product 1"})
    db.insert_product({"asin": "B001", "title": "Product 1 Updated"})
    results = db.get_all_products()
    assert len(results) == 1  # ✅ no duplicates