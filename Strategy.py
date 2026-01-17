from __future__ import annotations
from abc import ABC

class Strategy(ABC):
    def __init__(self):
        self.next_strategy : Strategy | None = None
        self.to_swap: bool = False

    def swap_strategy(self, new_strategy) -> Strategy:
        self.next_strategy = new_strategy
        self.to_swap = True