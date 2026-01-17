from abc import ABC, abstractmethod

from game_message import TeamGameState, Spawner


class SpawnerStrategy(ABC):
    @abstractmethod
    def get_action(self,spawner: Spawner, game_message: TeamGameState):
        pass
