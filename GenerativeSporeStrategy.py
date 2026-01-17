from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, SporeMoveToAction, Position
from Utils import get_distance


class GenerativeSporeStrategy(SporeStrategy):
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
            action = SporeMoveToAction(spore.id, best_target)
            return action

        return