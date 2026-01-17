import math
import typing

import Utils
import game_message
from CoverStrategy import CoverStrategy
from CreateSpawnerSporeStrategy import CreateSpawnerSporeStrategy
from GenerativeSporeStrategy import GenerativeSporeStrategy
from SpawnerStrategy import SpawnerStrategy
from SporeStrategy import SporeStrategy
from Strategyswapper import Strategyswapper
from SwappedStrat import SwappedStrat
from TallSpawnerStrategy import TallSpawnerStrategy
from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.spore_strategies: dict[str, SporeStrategy] = dict()
        self.spawner_strategies: dict[str, SpawnerStrategy] = dict()
        self.sporeStrategyQueue: dict[tuple[int, int], SporeStrategy] = {}
        self.spawnerStrategyQueue: dict[Position, SpawnerStrategy] = dict()
        self.strategySwapper = Strategyswapper()
        self.noSpawnersLastTick = 0

    def get_next_move(self, game_message: TeamGameState) -> list[Action]:
        self.clear_dead_strategies(game_message.world.teamInfos[game_message.yourTeamId])
        actions = self.run_strategies(game_message)
        self.swap_strategies_if_needed()
        return actions

    def create_spore_strategy(self, spore, game_message) -> SporeStrategy:
        key = (spore.position.x,spore.position.y)
        if key in self.sporeStrategyQueue:
            strategy = self.sporeStrategyQueue[key]
            self.sporeStrategyQueue.pop(key)
            return strategy

        if len(game_message.world.teamInfos[game_message.yourTeamId].spawners) == 0:
            target = self._find_spawner_position(game_message)
            return CreateSpawnerSporeStrategy(target,self.queue_spore_strategy)
        elif len(game_message.world.teamInfos[game_message.yourTeamId].spawners) < 3:
            target = self._find_spawner_position(game_message)
            return CreateSpawnerSporeStrategy(target,self.queue_spore_strategy)
        return GenerativeSporeStrategy()

    def _find_spawner_position(self, game_message):
        if len(game_message.world.teamInfos[game_message.yourTeamId].spawners) == 0:
            return game_message.world.teamInfos[game_message.yourTeamId].spores[0].position
        elif len(game_message.world.teamInfos[game_message.yourTeamId].spawners) < 3:
            current_spawner_position = game_message.world.teamInfos[game_message.yourTeamId].spawners[0].position
            return self._choose_target(current_spawner_position, game_message)

    def _choose_target(self, current_spawner_pos, game_message):
        for spore in game_message.world.teamInfos[game_message.yourTeamId].spores:
            if Utils.get_distance(current_spawner_pos, spore.position) >= 5:
                return spore.position
            else:
                x = int(math.copysign(1, spore.position.x - (spore.position.x + 5))) * (spore.position.x - (spore.position.x + 5))
                y = int(math.copysign(1, spore.position.y - (spore.position.y + 5))) * (spore.position.y - (spore.position.y + 5))
                return Position(x, y)

    def create_spawner_strategy(self, spawner, game_message) -> SpawnerStrategy:
        return TallSpawnerStrategy()

    def on_first_add_spore_and_spawners(self, team_info: TeamInfo,game_message: TeamGameState) -> None:
        for spore in team_info.spores:
            self.add_spore_strategy(spore.id, self.create_spore_strategy(spore, game_message))
        for spawner in team_info.spawners:
            self.add_spawner_strategy(spawner.id, self.create_spawner_strategy(spawner, game_message))

    def run_strategies(self, game_message: TeamGameState):
        actions = []
        team_info = game_message.world.teamInfos[game_message.yourTeamId]
        currentNbSpawners = len(game_message.world.teamInfos[game_message.yourTeamId].spawners)

        if self.noSpawnersLastTick > currentNbSpawners:
            spore = sorted(game_message.world.teamInfos[game_message.yourTeamId].spores, key=lambda sprout: sprout.biomass)[-2]
            self.spore_strategies[spore.id] = CreateSpawnerSporeStrategy(spore.position, self.queue_spore_strategy)
        self.noSpawnersLastTick = currentNbSpawners

        for spore in team_info.spores:
            if spore.id not in self.spore_strategies:
                sporeStrategy = self.create_spore_strategy(spore, game_message)
                self.add_spore_strategy(spore.id, sporeStrategy)
            strat = self.spore_strategies[spore.id]
            action = strat.get_action(spore, game_message)
            if action is not None:
                actions.append(action)
        for spawner in team_info.spawners:
            if spawner.id not in self.spawner_strategies:
                spawnerStrategy = self.create_spawner_strategy(spawner, game_message)
                self.add_spawner_strategy(spawner.id, spawnerStrategy)
            strat = self.spawner_strategies[spawner.id]
            action = strat.get_action(spawner, game_message)
            if action is not None:
                actions.append(action)
        return actions

    def add_spore_strategy(self, id: str, sporeStrategy: SporeStrategy):
        self.spore_strategies[id] = sporeStrategy

    def add_spawner_strategy(self, id: str, spawnerStrategy: SpawnerStrategy):
        self.spawner_strategies[id] = spawnerStrategy

    def clear_dead_strategies(self, team_info: TeamInfo):
        alive_spores = [spore.id for spore in team_info.spores]
        for spawner_id in list(self.spore_strategies.keys()):
            if spawner_id not in alive_spores:
                self.spore_strategies.pop(spawner_id)
        alive_spawners = [spawner.id for spawner in team_info.spawners]
        for spawner_id in list(self.spawner_strategies.keys()):
            if spawner_id not in alive_spawners:
                self.spawner_strategies.pop(spawner_id)

    def swap_strategies_if_needed(self):
        for key, value in self.spore_strategies.items():
            self.spore_strategies[key] = typing.cast(SporeStrategy, self.strategySwapper.swap_strategies_if_needed(value))
        for key, value in self.spawner_strategies.items():
            self.spawner_strategies[key] = typing.cast(SpawnerStrategy,self.strategySwapper.swap_strategies_if_needed(value))

    def queue_spore_strategy(self,position : Position, sporeStrategy: SporeStrategy):
        self.sporeStrategyQueue[(position.x,position.y)] = sporeStrategy