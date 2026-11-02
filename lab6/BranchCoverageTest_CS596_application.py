import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


def test_prohibited_category_true():
    with pytest.raises(ValueError):
        duty_rate("weapons", "FTA")


def test_prohibited_category_false():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_fta_true():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_fta_false():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta_true():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_fta_false():
    assert duty_rate("clothing", "US") == 0.12


def test_books_category():
    assert duty_rate("books", "US") == 0


def test_other_category():
    assert duty_rate("furniture", "US") == 0.15


def test_negative_value_true():
    with pytest.raises(ValueError):
        total_duty("electronics", -100, "US", False)


def test_negative_value_false():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_gift_true_below_limit():
    assert total_duty("electronics", 4000, "US", True) == 0


def test_gift_true_above_limit():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_gift_false_below_limit():
    assert total_duty("electronics", 500, "US", False) == 0


def test_gift_false_above_limit():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_minimum_duty_condition_true():
    assert total_duty("clothing", 5500, "FTA", True) == 50


def test_minimum_duty_condition_false():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_prohibited_clearance():
    assert clearance_channel(500, "weapons", True) == "refuse"


def test_non_prohibited_clearance():
    assert clearance_channel(500, "electronics", True) == "green"


def test_value_above_100000():
    assert clearance_channel(150000, "electronics", True) == "inspect"


def test_value_below_100000():
    assert clearance_channel(50000, "electronics", True) == "green"


def test_value_above_20000_without_documents():
    assert clearance_channel(25000, "electronics", False) == "inspect"


def test_value_above_20000_with_documents():
    assert clearance_channel(25000, "electronics", True) == "green"


def test_value_below_20000_without_documents():
    assert clearance_channel(10000, "electronics", False) == "green"