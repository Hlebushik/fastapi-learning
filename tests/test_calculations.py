import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
    (float('inf'), 1, float('inf')),])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0
    assert subtract(100, 50) == 50
    assert subtract(1, float('inf')) == -float('inf')

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 100) == 0
    assert multiply(5, 5) == 25
    assert multiply(float('inf'), 2) == float('inf')

def test_divide():
    assert divide(6, 3) == 2.0
    assert divide(5, 2) == 2.5
    assert divide(-10, 2) == -5.0
    assert divide(0, 1) == 0.0
    try:
        divide(1, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"
    assert divide(float('inf'), 1) == float('inf')


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100

def test_bank_default_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_bank_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 150
    bank_account.deposit(50)
    assert bank_account.balance == 200

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 110
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 121



@pytest.mark.parametrize("deposited, withdrew, expected", [
    (100, 50, 50),
    (50, 10, 40),
    (0, 0, 0),])
def test_bank_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_bank_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(150)