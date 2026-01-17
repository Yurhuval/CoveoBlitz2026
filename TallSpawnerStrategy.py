from SpawnerStrategy import SpawnerStrategy
from game_message import SpawnerProduceSporeAction, TeamGameState, Spawner


class TallSpawnerStrategy(SpawnerStrategy):
    def get_action(self, spawner: Spawner, game_message: TeamGameState):
        nutrients = game_message.world.teamInfos[game_message.yourTeamId].nutrients
        if nutrients > 0:
            return SpawnerProduceSporeAction(spawner.id, nutrients)
        return None

    def get_action_with_budget(self, spawner: Spawner, game_message: TeamGameState, budget: int):
        if budget > 0:
            return SpawnerProduceSporeAction(spawner.id, budget)
        return None