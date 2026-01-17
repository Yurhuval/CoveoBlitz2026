import math

from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, Position, SporeSplitAction


class CoverStrategy(SporeStrategy):
    def __init__(self,destination : Position):
        super().__init__()
        self.destination : Position = destination
    def get_action(self, spore: Spore, game_message: TeamGameState):
        direction = Position(0,math.copysign(1,spore.position.y - self.destination.y))
        remainingBio = max(1,spore.biomass - abs(spore.position.x - self.destination.x))
        splitAction = SporeSplitAction(spore.id,remainingBio,direction)
        return splitAction