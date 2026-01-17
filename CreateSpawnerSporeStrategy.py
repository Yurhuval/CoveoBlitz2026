from typing import Callable

from CoverStrategy import CoverStrategy
from GenerativeSporeStrategy import GenerativeSporeStrategy
from SpawnerBlitzStrategy import SpawnerBlitzStrategy
from SporeStrategy import SporeStrategy
from game_message import TeamGameState, Position, SporeCreateSpawnerAction, Spore, SporeMoveToAction


class CreateSpawnerSporeStrategy(SporeStrategy):
    def __init__(self, target, queueFunc : Callable):
        super().__init__()
        self.target = target
        self.queueFun = queueFunc
        if target == None:
            print("!")

    def get_action(self, spore: Spore, game_message: TeamGameState):
        team_info = game_message.world.teamInfos[game_message.yourTeamId]
        if spore.position == self.target and spore.position in [spawner.position for spawner in game_message.world.spawners]:
            self.swap_strategy(GenerativeSporeStrategy())
        if spore.position == self.target and spore.biomass > team_info.nextSpawnerCost:
            self.swap_strategy(GenerativeSporeStrategy())
            return SporeCreateSpawnerAction(spore.id)
        else:
            return SporeMoveToAction(spore.id, self.target)
