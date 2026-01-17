from SpawnerStrategy import SpawnerStrategy
from game_message import SpawnerProduceSporeAction, TeamGameState, Spawner


class TallSpawnerStrategy(SpawnerStrategy):
    def get_action(self, spawner: Spawner, game_message: TeamGameState):
        action = SpawnerProduceSporeAction(spawner.id,game_message.world.teamInfos[game_message.yourTeamId].nutrients)
        return action