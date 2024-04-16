from models import OrderBook
from db import get_session

def get_price_to_buy_10_btc(session=get_session()):
    """Calculate and return the price to buy 10 bitcoin."""
    asks = session.query(OrderBook).filter(
        OrderBook.order_type == 'ask',
        OrderBook.quantity <= 10,
        ).order_by(OrderBook.rate.asc()).all()

    cumulative_quantity = 0.0

    for ask in asks:
        cumulative_quantity += ask.quantity
        if cumulative_quantity >= 10:
            return ask.amount

    return None


def get_price_to_sell_10_btc(session=get_session()):
    """Calculate and return the price to sell 10 bitcoin."""
    bids = session.query(OrderBook).filter(
        OrderBook.order_type == 'bid',
        OrderBook.quantity <= 10,
        ).order_by(OrderBook.rate.desc()).all()

    cumulative_quantity = 0.0

    for bid in bids:
        cumulative_quantity += bid.quantity
        if cumulative_quantity >= 10:
            return bid.amount
    return None
