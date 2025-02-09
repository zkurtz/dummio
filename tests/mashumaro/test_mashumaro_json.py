from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from mashumaro.mixins.json import DataClassJSONMixin

from dummio.mashumaro.json import example, load, save


class Currency(Enum):
    """Example copied from https://github.com/Fatal1ty/mashumaro/blob/master/README.md."""

    USD = "USD"
    EUR = "EUR"


@dataclass
class CurrencyPosition:
    """Example copied from https://github.com/Fatal1ty/mashumaro/blob/master/README.md."""

    currency: Currency
    balance: float


@dataclass
class StockPosition:
    """Example copied from https://github.com/Fatal1ty/mashumaro/blob/master/README.md."""

    ticker: str
    name: str
    balance: int


@dataclass
class Portfolio(DataClassJSONMixin):
    """Example copied from https://github.com/Fatal1ty/mashumaro/blob/master/README.md."""

    currencies: list[CurrencyPosition]
    stocks: list[StockPosition]


def test_json(tmp_path: Path):
    # Example copied from https://github.com/Fatal1ty/mashumaro/blob/master/README.md:
    data = Portfolio(
        currencies=[
            CurrencyPosition(Currency.USD, 238.67),
            CurrencyPosition(Currency.EUR, 361.84),
        ],
        stocks=[
            StockPosition("AAPL", "Apple", 10),
            StockPosition("AMZN", "Amazon", 10),
        ],
    )
    filepath = tmp_path / "data.json"
    save(data, filepath=filepath)
    loaded_data = load(filepath=filepath, model=Portfolio)
    assert data == loaded_data

    # Also run the example:
    example(filepath=filepath)
