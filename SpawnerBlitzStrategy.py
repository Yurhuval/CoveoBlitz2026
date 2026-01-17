import math
from typing import Callable

import Utils
from MoveStrategy import MoveStrategy
from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, Spawner, Position, SporeMoveToAction


class SpawnerBlitzStrategy(SporeStrategy):
    def __init__(self, queueFunc : Callable, destination: Position = None, ):
        super().__init__()
        self.destination : Position = None
        self.queueFunc = queueFunc
    def get_action(self, spore: Spore, game_message: TeamGameState):
        if self.destination is None or spore.position == self.destination:
            self.destination = self.find_destination(spore,game_message)
        return SporeMoveToAction(spore.id,self.destination)

    def find_destination(self, spore: Spore, game_message: TeamGameState) -> Position:
        team_info = game_message.world.teamInfos[game_message.yourTeamId]
        max_dist = math.inf
        destination = None
        for spawner in [spawner for spawner in game_message.world.spawners if spawner not in team_info.spawners]:
            dist = Utils.get_distance(spore.position, spawner.position)
            if max_dist > dist > 0:
                max_dist = dist
                destination = spawner.position

        return destination


