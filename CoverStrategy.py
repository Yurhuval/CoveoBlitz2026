import math
from collections.abc import Callable

from MoveStrategy import MoveStrategy
from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, Position, SporeSplitAction


class CoverStrategy(SporeStrategy):
    def __init__(self,destination : Position,queueFunc : Callable):
        super().__init__()
        self.destination : Position = destination
        self.queueFunc : Callable = queueFunc
    def get_action(self, spore: Spore, game_message: TeamGameState):
        direction = Position(0,-int(math.copysign(1,spore.position.y - self.destination.y)))
        remainingBio = max(1,spore.biomass - abs(spore.position.x - self.destination.x))
        splitAction = SporeSplitAction(spore.id,remainingBio,direction)
        self.queueFunc(spore.position, MoveStrategy(Position(spore.position.x, self.destination.x)))
        return splitAction