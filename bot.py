import typing

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
        elif game_message.world.teamInfos[game_message.yourTeamId].nutrients > game_message.world.teamInfos[game_message.yourTeamId].nextSpawnerCost + 20:

            targets = self._find_spawner_position(game_message)
            target = self._choose_target(targets, game_message)
            return CreateSpawnerSporeStrategy(target,self.queue_spore_strategy)
        return GenerativeSporeStrategy()

    def _find_spawner_position(self, game_message):
        if not game_message.world.teamInfos[game_message.yourTeamId].spawners:
            return game_message.world.teamInfos[game_message.yourTeamId].spores[0].position
        else:
            position = game_message.world.teamInfos[game_message.yourTeamId].spawners[0].position
            x_left = position.x + 5
            x_right = position.x - 5
            y_top = position.y + 5
            y_bottom = position.y - 5

            return [Position(x_left, position.y), Position(position.x, y_top), Position(x_right, position.y), Position(position.x, y_bottom)]

    def _choose_target(self, targets, game_message):
        pass

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
        if game_message.tick == 1:
            self.on_first_add_spore_and_spawners(team_info,game_message)

        for spore in team_info.spores:
            if spore.id not in self.spore_strategies:
                sporeStrategy = self.create_spore_strategy(spore, game_message)
                self.add_spore_strategy(spore.id, sporeStrategy)
            strat = self.spore_strategies[spore.id]
            actions.append(strat.get_action(spore, game_message))
        for spawner in team_info.spawners:
            if spawner.id not in self.spawner_strategies:
                spawnerStrategy = self.create_spawner_strategy(spawner, game_message)
                self.add_spawner_strategy(spawner.id, spawnerStrategy)
            strat = self.spawner_strategies[spawner.id]
            actions.append(strat.get_action(spawner, game_message))
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