from SporeStrategy import SporeStrategy
from game_message import TeamGameState, Position, SporeCreateSpawnerAction, Spore, SporeMoveToAction


class CreateSpawnerSporeStrategy(SporeStrategy):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def get_action(self, spore: Spore, game_message: TeamGameState):
        if spore.position == self.target:
            return SporeCreateSpawnerAction(spore.id)
        else:
            return SporeMoveToAction(spore.id, self.target)
