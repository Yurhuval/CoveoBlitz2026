from SporeStrategy import SporeStrategy
from game_message import TeamGameState, Position, SporeCreateSpawnerAction, Spore


class CreateSpawnerSporeStrategy(SporeStrategy):
    def __init__(self, position):
        super().__init__()
        self.position = position

    def get_action(self, spore: Spore, game_message: TeamGameState):
        if spore.position == self.position:
            return SporeCreateSpawnerAction(spore.id)
        else:
            return SporeCreateSpawnerAction(self.position)
