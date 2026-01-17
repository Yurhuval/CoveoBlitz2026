from abc import ABC, abstractmethod

from game_message import TeamGameState


class SporeStrategy(ABC):
    @abstractmethod
    def get_action(sporeId: str,game_message : TeamGameState ):
        pass

