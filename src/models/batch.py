from datetime import date
from typing import Optional, Self

from src.models.order_line import OrderLine


class Batch:
    reference: str
    sku: str  # stock-keeping unit
    eta: Optional[date]
    _purchased_quantity: int
    _allocations: set[OrderLine]

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: Optional[date],
    ):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(order_line.quantity for order_line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku \
            and self.available_quantity >= order_line.quantity

    def allocate(self, order_line: OrderLine):
        if not self.can_allocate(order_line):
            return
        self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line not in self._allocations:
            return
        self._allocations.remove(order_line)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __gt__(self, other: Self) -> bool:
        if self.eta is None:
            return False
        elif other.eta is None:
            return True
        return self.eta > other.eta

    def __hash__(self) -> int:
        return hash(self.reference)

    def __repr__(self) -> str:
        return f'<Batch {self.reference}>'
