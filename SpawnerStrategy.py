from abc import abstractmethod

from Strategy import Strategy
from game_message import TeamGameState, Spawner


class SpawnerStrategy(Strategy):
    @abstractmethod
    def get_action(self,spawner: Spawner, game_message: TeamGameState):
        pass
