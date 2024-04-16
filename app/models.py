from datetime import datetime
from sqlalchemy import Column, Float, DateTime, Integer, Enum, event
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now(),
                        nullable=False, comment="Current datetime")


class OrderBook(TimestampModel):
    __tablename__ = 'price_action'
    epoch_time = Column(Integer, nullable=False)
    order_type = Column(Enum('ask', 'bid'), nullable=False,
                        comment="Choose between 'ask' or 'bid'")
    amount = Column(Float, nullable=False, comment="Enter Amount")
    quantity = Column(Float, nullable=False, comment="Enter Quantity")
    exchange = Column(Enum('Coinbase', 'Gemini', 'Kraken'), nullable=False,
                      comment="Choose between 'coinbase', 'gemini' or 'Kraken'")
    rate = Column(Float, nullable=False, comment="Amount per Quantity")

    def __repr__(self):
        date_obj = datetime.fromtimestamp(self.epoch_time)

        return f"<PriceAction(Time={date_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}, \
OrderType={self.order_type}, Amount={self.amount}, \
Quantity={self.quantity}, Exchange={self.exchange})>"
