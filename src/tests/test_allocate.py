from datetime import date, timedelta

import pytest

from src.helpers.allocate import OutOfStock, allocate
from src.models.batch import Batch
from src.models.order_line import OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=tomorrow)
    order_line = OrderLine('order-ref', 'RETRO-CLOCK', 10)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today)
    medium = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow)
    latest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=later)
    order_line = OrderLine('order-ref', 'MINIMALIST-SPOON', 10)

    allocate(order_line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-batch', 'HIGHBROW-POSTER', 100, eta=None)
    shipment_batch = Batch(
        'shipment-batch',
        'HIGHBROW-POSTER',
        100,
        eta=tomorrow,
    )
    order_line = OrderLine('order-ref', 'HIGHBROW-POSTER', 10)

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_if_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    order_line = OrderLine('order-1', 'SMALL-FORK', 10)
    order_line2 = OrderLine('order-2', 'SMALL-FORK', 1)

    allocate(order_line, [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(order_line2, [batch])
