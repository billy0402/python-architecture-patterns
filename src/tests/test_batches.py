from datetime import date

from src.models.batch import Batch
from src.models.order_line import OrderLine

today = date.today()


def create_batch_and_order_line(
    sku: str,
    batch_quantity: int,
    order_line_quantity: int,
):
    return (
        Batch('batch-001', sku, batch_quantity, eta=today),
        OrderLine('order-ref', sku, order_line_quantity),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = create_batch_and_order_line('SMALL-TABLE', 20, 2)

    batch.allocate(order_line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_order_line = create_batch_and_order_line(
        'ELEPHANT-LAMP',
        20,
        2,
    )

    assert large_batch.can_allocate(small_order_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_order_line = create_batch_and_order_line(
        'ELEPHANT-LAMP',
        2,
        20,
    )

    assert small_batch.can_allocate(large_order_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, order_line = create_batch_and_order_line('ELEPHANT-LAMP', 2, 2)

    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch-001', 'UNCOMFORTABLE_CHAIR', 100, eta=None)
    different_sku_order_line = OrderLine('order-ref', 'EXPENSIVE-TOASTER', 10)

    assert batch.can_allocate(different_sku_order_line) is False


def test_allocations_is_idempotent():
    batch, order_line = create_batch_and_order_line('ANGULAR-DESK', 20, 2)

    batch.allocate(order_line)
    batch.allocate(order_line)

    assert batch.available_quantity == 18


def test_deallocate():
    batch, order_line = create_batch_and_order_line(
        'EXPENSIVE-FOOTSTOOL',
        20,
        2,
    )

    batch.allocate(order_line)
    batch.deallocate(order_line)

    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_order_line = create_batch_and_order_line(
        'DEALLOCATE-TRINKET',
        20,
        2,
    )

    batch.deallocate(unallocated_order_line)

    assert batch.available_quantity == 20
