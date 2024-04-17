from models import OrderBook
from db import get_session

def get_price_to_buy_btc(required_qty=10, session=get_session()):
    """Calculate and return the cost to buy bitcoin using knapsack algorithm."""
    asks = session.query(OrderBook).filter(
        OrderBook.order_type == 'ask',
        OrderBook.quantity <= required_qty
    ).order_by(OrderBook.quantity.desc(),OrderBook.rate.asc()).all()
    
    if asks:
        cumulative_quantity = 0
        cumulative_amount = 0
        chosen_orders = []

        for i in asks:
            if cumulative_quantity <= required_qty:
                if i.quantity <= (required_qty - cumulative_quantity):
                    cumulative_quantity += i.quantity
                    cumulative_amount += i.amount
                    chosen_orders.append((i,cumulative_quantity,cumulative_amount))
            else:
                break

        print(f"chosen_asks: \n{chosen_orders}")
        return cumulative_amount, cumulative_quantity
    return None, None

def get_price_to_sell_btc(required_qty=10, session=get_session()):
    """Calculate and return the revenue to sell bitcoin using knapsack algorithm."""
    bids = session.query(OrderBook).filter(
        OrderBook.order_type == 'bid',
        OrderBook.quantity <= required_qty
    ).order_by(OrderBook.quantity.desc(),OrderBook.rate.desc()).all()
    
    if bids:
        cumulative_quantity = 0
        cumulative_amount = 0
        chosen_orders = []

        for i in bids:
            if cumulative_quantity <= required_qty:
                if i.quantity <= (required_qty - cumulative_quantity):
                    cumulative_quantity += i.quantity
                    cumulative_amount += i.amount
                    chosen_orders.append((i,cumulative_quantity,cumulative_amount))
            else:
                break
        print(f"chosen_bids: \n{chosen_orders}")
        return cumulative_amount, cumulative_quantity
    return None, None
