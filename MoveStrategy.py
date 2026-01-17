from SporeStrategy import SporeStrategy
from game_message import Position, Spore, SporeMoveToAction, TeamGameState


class MoveStrategy(SporeStrategy):
    def __init__(self,destination: Position):
        super().__init__()
        self.destination = destination


    def get_action(self, spore: Spore, game_message: TeamGameState):
        return SporeMoveToAction(spore.id,self.destination)