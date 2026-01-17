from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, SporeMoveToAction, SporeMoveAction, Position


class GenerativeSporeStrategy(SporeStrategy):
    def get_action(self, spore: Spore, game_message: TeamGameState):
        position = spore.position
        return SporeMoveAction(Position(0,1))
