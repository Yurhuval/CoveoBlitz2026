from SpawnerBlitzStrategy import SpawnerBlitzStrategy
from SporeStrategy import SporeStrategy
from Utils import get_distance
from game_message import SporeMoveToAction, Position, Spore, TeamGameState


class GenerativeSporeStrategy(SporeStrategy):
    def __init__(self):
        super().__init__()
        self.path = None
    def get_action(self, spore: Spore, game_message: TeamGameState):
        world = game_message.world
        game_map = world.map

        if spore.biomass < 2:
            return None

        best_target = None
        min_dist = float('inf')
        for y in range(game_map.height):
            for x in range(game_map.width):
                nutrient_value = game_map.nutrientGrid[x][y]
                if nutrient_value > 0 and world.ownershipGrid[x][y] != game_message.yourTeamId:
                    target_pos = Position(x, y)
                    dist = get_distance(spore.position, target_pos)

                    if dist < min_dist:
                        min_dist = dist
                        best_target = target_pos
        if best_target:

            self.calculatePath(spore.position, best_target,game_message)
            if spore.position == self.target:
                self.recalculate_path(spore.position,best_target,game_message)

            action = SporeMoveToAction(spore.id, self.next_step(spore.position))
            return action

        next_strat = SpawnerBlitzStrategy()
        next_strat.next_strategy = GenerativeSporeStrategy()
        self.swap_strategy(next_strat)

        return None