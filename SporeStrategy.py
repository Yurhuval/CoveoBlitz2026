from abc import ABC, abstractmethod

from Strategy import Strategy
from game_message import TeamGameState, Spore


class SporeStrategy(Strategy):
    @abstractmethod
    def get_action(self,spore : Spore, game_message : TeamGameState):
        pass

