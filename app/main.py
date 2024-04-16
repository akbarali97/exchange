import argparse
from get_orders import Order
from db import get_session, initialize_database
from helpers import *

def main():
    # Initialize the database session
    session = get_session()
    # Run the code in a loop
    while True:
        try:
            # Prompt the user for input on exchanges and quantity
            exchanges = input("Please enter a comma-separated list of exchanges (or press Ctrl + D to exit): ").strip()
            quantity_str = input("Please enter the quantity (or press Ctrl + D to exit): ").strip()

            # Handle empty input
            if not exchanges or not quantity_str:
                print("Invalid input. Please provide valid exchanges and quantity.")
                continue

            # Parse the exchanges and quantity
            exchanges_list = exchanges.split(',')
            quantity = int(quantity_str)

            print(f"Exchanges: {exchanges_list}")

            # Create an instance of the Order class
            order_obj = Order()

            # Fetch orders based on the provided exchanges
            orders = order_obj.orders(exchanges=exchanges_list)

            # Add all fetched orders to the session and commit
            session.add_all(orders)
            session.commit()

            # Perform the necessary operations with the quantity
            if quantity:
                buy_amount, buy_qty = get_price_to_buy_btc(required_qty=quantity)
                print(f'Price to buy {buy_qty} bitcoins: {buy_amount}')

                sell_amount, sell_qty = get_price_to_sell_btc(required_qty=quantity)
                print(f'Price to sell {sell_qty} bitcoins: {sell_amount}')
            print('\n\n\n')
        # Handle Ctrl + D (EOFError) gracefully to exit the loop
        except EOFError:
            print("\nEnd of input detected. Exiting the program.")
            break
        # Handle invalid quantity input (ValueError)
        except ValueError:
            print("Invalid quantity entered. Please enter a numeric value.")

if __name__ == "__main__":
    # Initialize the database
    initialize_database()
    
    # Run the main function
    main()
