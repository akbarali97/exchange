import asyncio
import websockets
import json
from datetime import datetime


import requests
from constant import endpoints
from models import OrderBook

class Order:

    def gemini_orders(self):
        res = requests.get(endpoints['gemini']['api'])
        data = res.json()
        orders = []
        for order_type, _list in data.items():
            order_type = 'ask' if order_type == 'asks' else 'bid'
            for i in _list:
                quantity=float(i['amount'])
                amount=float(i['price'])
                rate = amount / quantity if quantity > 0 else 0
                orders.append(OrderBook(
                                epoch_time=int(i['timestamp']), 
                                order_type=order_type,
                                quantity=quantity,
                                amount=amount,
                                rate=rate,
                                exchange='Gemini'))
        return orders

    def coinbase_orders(self):
        orders = []
        async def connect_to_websocket():
            async with websockets.connect(endpoints['coinbase']['api']) as websocket:
                await websocket.send(json.dumps({
                    "type": "subscribe",
                    "product_ids": ["BTC-USD"],
                    "channels": ["level2_batch"]}))

                # NOTE: response type
                '''
                {
                "type": "snapshot",
                "product_id": "BTC-USD",
                "bids": [["10101.10", "0.45054140"]],
                "asks": [["10102.55", "0.57753524"]]
                }
                '''
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data['type'] == 'snapshot':
                        break

                date_obj = datetime.fromisoformat(data['time'].rstrip("Z"))

                for i in data['bids']:
                    amount = float(i[0])
                    quantity=float(i[1])
                    rate = amount / quantity if quantity > 0 else 0
                    orders.append(OrderBook(
                    epoch_time=date_obj.timestamp(),
                    order_type='bid',
                    quantity=quantity,  
                    amount=amount,
                    rate = rate,
                    exchange='Coinbase'))

                for i in data['asks']:
                    amount = float(i[0])
                    quantity=float(i[1])
                    rate = amount / quantity if quantity > 0 else 0
                    orders.append(OrderBook(
                    epoch_time=date_obj.timestamp(),
                    order_type='ask',
                    quantity=quantity,  
                    amount=amount,
                    rate = rate,
                    exchange='Coinbase'))

        asyncio.run(connect_to_websocket())
        return orders


    def kraken_orders(self):
        orders = []
        res = requests.get(endpoints['kraken']['api'])
        data = res.json()

        asks = data['result']['XXBTZUSD']['asks']
        bids = data['result']['XXBTZUSD']['bids']

        for ask in asks:
            amount = float(ask[0])
            quantity = float(ask[1])
            epoch_time = int(ask[2])
            rate = amount / quantity if quantity > 0 else 0
            
            order_book_entry = OrderBook(
                epoch_time=epoch_time,
                order_type='ask',
                amount=amount,
                quantity=quantity,
                rate=rate,
                exchange='Kraken')
            
            orders.append(order_book_entry)

        for bid in bids:
            amount = float(bid[0])
            quantity = float(bid[1])
            epoch_time = int(bid[2])
            rate = amount / quantity if quantity > 0 else 0

            order_book_entry = OrderBook(
                epoch_time=epoch_time,
                order_type='bid',
                amount=amount,
                quantity=quantity,
                rate=rate,
                exchange='Kraken',
            )
            orders.append(order_book_entry)

        return orders


    def orders(self, exchanges=['Kraken', 'Gemini', 'Coinbase']):
        orders = []
        if 'Coinbase' in exchanges:
            orders.extend(self.coinbase_orders())
        if 'Gemini' in exchanges:
            orders.extend(self.gemini_orders())
        if 'Kraken' in exchanges:
            orders.extend(self.kraken_orders())
        return orders