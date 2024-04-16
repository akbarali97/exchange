import sys
import argparse
from get_orders import Order
from db import get_session, initialize_database
from helpers import *

def main():
    session = get_session()

    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Run the app.")
    parser.add_argument("--show-log", action="store_true", help="Show logs")
    parser.add_argument("--exchanges", type=str,
                        help="Comma-separated list of exchanges")
    parsed_args = parser.parse_args(args)

    parsed_args.show_log
    parsed_args.exchanges

    order_obj = Order()

    session.add_all(order_obj.orders())
    session.commit()

    # # Query to filter and sort bids (highest price first)
    # bids = session.query(OrderBook).filter(OrderBook.order_type == 'bid').order_by(
    #     OrderBook.amount.desc()).limit(10).all()

    # # Query to filter and sort asks (lowest price first)
    # asks = session.query(OrderBook).filter(OrderBook.order_type == 'ask').order_by(
    #     OrderBook.amount.asc()).limit(10).all()

    # # Print sorted bids and asks
    # print('\n\n\n')
    # print('========================== Bids ==========================')
    # for bid in bids:
    #     print(bid)

    # print('\n\n\n')
    # print('========================== Asks ==========================')
    # for ask in asks:
    #     print(ask)


    print('\n\n\n')
    print(f'price to Buy 10 bitcoins: {get_price_to_buy_10_btc()}')
    print(f'price to Sell 10 bitcoins: {get_price_to_sell_10_btc()}')

if __name__ == "__main__":
    initialize_database()
    main()
