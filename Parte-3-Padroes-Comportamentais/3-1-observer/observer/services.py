from dataclasses import dataclass
from typing import Callable, Dict
from .signals import price_changed, subscribe as _subscribe, unsubscribe_all as _unsubscribe_all

class StockMarket:
    def __init__(self):
        self._prices: Dict[str, float] = {}

    def set_price(self, symbol: str, price: float):
        old = self._prices.get(symbol)
        self._prices[symbol] = price
        price_changed.send(sender=self.__class__, symbol=symbol, old=old, price=price)

def subscribe(symbol: str, obs_type: str, observer):
    _subscribe(symbol, obs_type, observer)

def unsubscribe(symbol: str, obs_type: str | None = None):
    _unsubscribe_all(symbol, obs_type)

@dataclass
class SMSObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[SMS] {evt['symbol']} {evt['old']} -> {evt['price']}")

@dataclass
class EmailObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[EMAIL] {evt['symbol']} = {evt['price']}")

@dataclass
class DashboardObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[DASH] {evt['symbol']}: {evt['price']}")

market = StockMarket()
