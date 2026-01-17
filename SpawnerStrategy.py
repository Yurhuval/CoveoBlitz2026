from abc import ABC, abstractmethod

from game_message import TeamGameState


class SpawnerStrategy(ABC):
    @abstractmethod
    def get_action(spawnerId : str, game_message : TeamGameState ):
        pass
