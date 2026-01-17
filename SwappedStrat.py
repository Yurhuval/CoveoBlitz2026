from SpawnerStrategy import SpawnerStrategy
from TallSpawnerStrategy import TallSpawnerStrategy
from game_message import Spawner, TeamGameState, SpawnerProduceSporeAction


class SwappedStrat(SpawnerStrategy):
    def get_action(self, spawner: Spawner, game_message: TeamGameState):
        self.swap_strategy(TallSpawnerStrategy())
        return SpawnerProduceSporeAction(spawner.id,game_message.world.teamInfos[game_message.yourTeamId].nutrients)