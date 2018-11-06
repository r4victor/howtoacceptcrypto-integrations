from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class Currency:
    name: str
    code: str
    sign: str
    subunit_factor: int

    def __post_init__(self):
        self.decimal_len = round(math.log(self.subunit_factor, 10))


@dataclass
class Money:
    currency: Currency
    amount: int

    def __post_init__(self):
        self.units = self.amount // self.currency.subunit_factor
        self.subunits = self.amount % self.currency.subunit_factor

    def __str__(self):
        return f'{self.currency.sign}{self.decimal_repr()}'

    def decimal_repr(self) -> str:
        return f'{self.units}.{str(self.subunits).zfill(self.currency.decimal_len)}'

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError('Different currencies')
        return Money(self.currency, self.amount+other.amount)

    def __sub__(self, other: Money) -> Money:
        return self + (-1) * other

    def __mul__(self, factor: int) -> Money:
        return Money(self.currency, factor*self.amount)

    def __rmul__(self, factor: int) -> Money:
        return self * factor

    def __le__(self, other):
        if self.currency != other.currency:
            raise ValueError('Different currencies')
        return self.amount <= other.amount

    def __lt__(self, other):
        return self <= other and self != other


USD = Currency(name='United States dollar', code='USD', sign='$', subunit_factor=100)
EUR = Currency(name='Euro', code='EUR', sign='€', subunit_factor=100)
GBP = Currency(name='Pound sterling', code='GBP', sign='£', subunit_factor=100)
# ISO 4217 for Bitcoin is XBT, but most of the processor use BTC
BTC = Currency(name='Bitcoin', code='BTC', sign='₿', subunit_factor=100000000)



    