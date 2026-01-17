from SpawnerBlitzStrategy import SpawnerBlitzStrategy
from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, SporeMoveAction, Position, SporeSplitAction
from Utils import get_distance, get_enemy_position_dict
from collections import deque


DIRS = [Position(0, -1),Position(0, 1),Position(-1, 0),Position(1, 0)]

class GenerativeSporeStrategy(SporeStrategy):
    visited_positions = set()
    consumed_nutrients = set()

    def __init__(self):
        super().__init__()
        self.last_pos = None
        self.stuck_count = 0
        self.current_pos = None
        self.current_targets = []
        self.target = None

    def set_current_targets(self, targets):
        self.current_targets = targets

    def _find_path_to_nutrient_dijikstra(self, start: Position, game_map, world, my_team_id):
        queue = deque([(start, [])])
        visited = { (start.x, start.y) }

        while queue:
            curr_pos, path = queue.popleft()
            if game_map.nutrientGrid[curr_pos.x][curr_pos.y] > 0 and (curr_pos.x, curr_pos.y) not in GenerativeSporeStrategy.consumed_nutrients:
                return path[0] if path else None

            for d in DIRS:
                nx, ny = curr_pos.x + d.x, curr_pos.y + d.y
                if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        new_path = path + [d]
                        queue.append((Position(nx, ny), new_path))
        return None

    def get_action(self, spore: Spore, game_message: TeamGameState):
        world = game_message.world
        game_map = world.map
        my_team_id = game_message.yourTeamId

        if game_map.nutrientGrid[spore.position.x][spore.position.y] > 0:
            GenerativeSporeStrategy.consumed_nutrients.add((spore.position.x, spore.position.y))

        if self.current_pos and self.current_pos.x == spore.position.x and self.current_pos.y == spore.position.y:
            self.stuck_count += 1
        else:
            self.stuck_count = 0
        self.current_pos = spore.position

        best_direction = self._find_path_to_nutrient_dijikstra(spore.position, game_map, world, my_team_id)

        #si il y a aucun chemin direct vers un nutriment on reprend avec le score
        if not best_direction or self.stuck_count > 0:
            max_score = -float('inf')
            enemies_dict = get_enemy_position_dict(world, my_team_id)

            for d in DIRS:
                nx, ny = spore.position.x + d.x, spore.position.y + d.y

                if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                    score = 0
                    nutrients = game_map.nutrientGrid[nx][ny]

                    #condition pour les nutriments
                    if nutrients > 0 and (nx, ny) not in GenerativeSporeStrategy.consumed_nutrients:
                        score += 10000 + nutrients * 100
                    elif (nx, ny) in GenerativeSporeStrategy.consumed_nutrients:
                        score -= 50

                    owner = world.ownershipGrid[nx][ny]
                    biomass = world.biomassGrid[nx][ny]

                    #expansion
                    if owner != my_team_id:
                        score += 10
                        if biomass > 0:
                            score += 5

                    #évitement ennemis plus forts que nous
                    enemy = enemies_dict.get((nx, ny))
                    if enemy:
                        if enemy.biomass < spore.biomass:
                            score += 50
                        else:
                            score -= 500

                    #évité les alliés (dispersion)
                    for target in self.current_targets:
                        if target.x == nx and target.y == ny:
                            score -= 50

                    #condition pour pas reculer
                    if self.last_pos and nx == self.last_pos.x and ny == self.last_pos.y:
                        score -= 100

                    #condition si bloqué
                    if self.stuck_count > 0:
                        import random
                        score += random.randint(0, 50)
                        if self.last_pos and nx == self.last_pos.x and ny == self.last_pos.y:
                            score += 150

                    if score > max_score:
                        max_score = score
                        best_direction = d

        if best_direction:
            self.last_pos = spore.position
            self.target = Position(spore.position.x + best_direction.x, spore.position.y + best_direction.y)
            if spore.biomass >= 6:
                return SporeSplitAction(spore.id, spore.biomass // 2, best_direction)
            return SporeMoveAction(spore.id, best_direction)

        return None