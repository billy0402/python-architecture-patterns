from src.models.batch import Batch
from src.models.order_line import OrderLine


class OutOfStock(Exception):
    pass


def allocate(order_line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            _batch for _batch in batches if _batch.can_allocate(order_line)
        )
        batch.allocate(order_line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {order_line.sku}')
