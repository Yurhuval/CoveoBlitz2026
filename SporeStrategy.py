from abc import ABC, abstractmethod

from game_message import TeamGameState, Spore


class SporeStrategy(ABC):
    @abstractmethod
    def get_action(self,spore : Spore, game_message : TeamGameState):
        pass
