from dataclasses import dataclass
from typing import Callable

@dataclass
class SMSObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[SMS] Produto {evt['name']} voltou ao estoque: {evt['stock']} unidades.")

@dataclass
class EmailObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[EMAIL] {evt['name']} disponível. Estoque: {evt['stock']}.")

@dataclass
class DashboardObserver:
    out: Callable = print
    def __call__(self, evt):
        self.out(f"[DASH] {evt['productId']} - {evt['name']} stock={evt['stock']}")
