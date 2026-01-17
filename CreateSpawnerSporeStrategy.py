from SporeStrategy import SporeStrategy
from game_message import TeamGameState, Position, SporeCreateSpawnerAction, Spore


class CreateSpawnerSporeStrategy(SporeStrategy):
    def get_action(self, spore: Spore, game_message: TeamGameState):
        return SporeCreateSpawnerAction(spore.id)

    def find_spawner_position(self, game_message: TeamGameState) -> Spore:
        if not game_message.world.teamInfos[game_message.yourTeamId].spawners:
            return game_message.world.spawners[game_message.yourTeamId].spores[0]