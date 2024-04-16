from models import OrderBook
from db import get_session

def get_price_to_buy_btc(required_qty=10,session=get_session()):
    """Calculate and return the price to buy bitcoin."""
    asks = session.query(OrderBook).filter(
        OrderBook.order_type == 'ask',
        OrderBook.quantity <= required_qty,
        ).order_by(OrderBook.rate.asc(),OrderBook.quantity.asc()).all()

    cumulative_quantity = 0.0
    cumulative_amount = 0.0

    for ask in asks:
        # print(ask)
        cumulative_quantity += ask.quantity
        cumulative_amount += ask.amount
        if cumulative_quantity >= required_qty:
            return cumulative_amount, cumulative_quantity

    return None


def get_price_to_sell_btc(required_qty=10,session=get_session()):
    """Calculate and return the price to sell bitcoin."""
    bids = session.query(OrderBook).filter(
        OrderBook.order_type == 'bid',
        OrderBook.quantity <= required_qty,
        ).order_by(OrderBook.rate.desc(), OrderBook.quantity.asc()).all()

    cumulative_quantity = 0.0
    cumulative_amount = 0.0

    for bid in bids:
        # print(bid)
        cumulative_quantity += bid.quantity
        cumulative_amount += bid.amount

        if cumulative_quantity >= required_qty:
            return cumulative_amount, cumulative_quantity
    return None
