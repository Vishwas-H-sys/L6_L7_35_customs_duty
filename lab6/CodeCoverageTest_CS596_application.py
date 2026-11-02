import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta():
    assert duty_rate("clothing", "US") == 0.12


def test_other_category():
    assert duty_rate("furniture", "US") == 0.15


def test_prohibited_weapons():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")


def test_prohibited_narcotics():
    with pytest.raises(ValueError):
        duty_rate("narcotics", "US")


def test_negative_value():
    with pytest.raises(ValueError):
        total_duty("electronics", -100, "US", False)


def test_gift_below_5000():
    assert total_duty("electronics", 4000, "US", True) == 0


def test_gift_equal_5000():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_above_5000_minimum_duty():
    assert total_duty("clothing", 5500, "FTA", True) == 50


def test_gift_above_5000_normal_duty():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_non_gift_below_1000():
    assert total_duty("electronics", 500, "US", False) == 0


def test_non_gift_equal_1000():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_non_gift_above_1000():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_gift_books_zero_duty():
    assert total_duty("books", 6000, "US", True) == 0


def test_clearance_prohibited():
    assert clearance_channel(500, "weapons", True) == "refuse"


def test_clearance_above_100000():
    assert clearance_channel(150000, "electronics", True) == "inspect"


def test_clearance_above_20000_without_documents():
    assert clearance_channel(25000, "electronics", False) == "inspect"


def test_clearance_above_20000_with_documents():
    assert clearance_channel(25000, "electronics", True) == "green"


def test_clearance_below_threshold():
    assert clearance_channel(10000, "electronics", False) == "green"