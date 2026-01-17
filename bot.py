import game_message
from GenerativeSporeStrategy import GenerativeSporeStrategy
from SpawnerStrategy import SpawnerStrategy
from SporeStrategy import SporeStrategy
from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.spore_strategies : dict[str, SporeStrategy] = dict()
        self.spawner_strategies : dict[str, SpawnerStrategy] = dict()
        self.sporeStrategyQueue : dict[Position, SporeStrategy] = dict()
        self.spawnerStrategyQueue : dict[Position, SpawnerStrategy] = dict()

    def get_next_move(self, game_message: TeamGameState) -> list[Action]:
        self.clear_dead_strategies(game_message.world.teamInfos[game_message.yourTeamId])
        actions = self.run_strategies(game_message)
        return actions

    def create_spore_strategy(self, spore, game_message) -> SporeStrategy:
        return GenerativeSporeStrategy()

    def create_spawner_strategy(self, spawner, game_message) -> SpawnerStrategy:
        pass

    def on_first_add_spore_and_spawners(self, team_info: TeamInfo):
        for spore in team_info.spores:
            self.add_spore_strategy(spore.id, self.create_spore_strategy(spore, game_message))
        for spawner in team_info.spawners:
            self.add_spawner_strategy(spawner.id, self.create_spawner_strategy(spawner, game_message))
    def run_strategies(self, game_message: TeamGameState):
        actions = []
        team_info = game_message.world.teamInfos[game_message.yourTeamId]
        if game_message.tick == 1 :
            self.on_first_add_spore_and_spawners(team_info)

        for spore in team_info.spores:
            if self.spore_strategies[spore.id] is None:
                sporeStrategy = self.create_spore_strategy(spore, game_message)
                self.add_spore_strategy(spore.id, sporeStrategy)
            strat = self.spore_strategies[spore.id]
            actions.append(strat.get_action(spore, game_message))
        for spawner in team_info.spawners:
            if self.spawner_strategies[spawner.id] is None:
                spawnerStrategy = self.create_spawner_strategy(spawner, game_message)
                self.add_spawner_strategy(spawner.id, spawnerStrategy)
            strat = self.spawner_strategies[spawner.id]
            actions.append(strat.get_action(spawner, game_message))
        return actions

    def add_spore_strategy(self, id : str, sporeStrategy : SporeStrategy):
        self.spore_strategies[id] = sporeStrategy

    def add_spawner_strategy(self, id : str, spawnerStrategy : SpawnerStrategy):
        self.spawner_strategies[id] = spawnerStrategy

    def clear_dead_strategies(self,team_info: TeamInfo):
        alive_spores = [spore.id for spore in team_info.spores]
        for spawner_id in list(self.spore_strategies.keys()):
            if spawner_id not in alive_spores:
                self.spore_strategies.pop(spawner_id)
        alive_spawners = [spawner.id for spawner in team_info.spawners]
        for spawner_id in list(self.spawner_strategies.keys()):
            if spawner_id not in alive_spawners:
                self.spawner_strategies.pop(spawner_id)
