from SporeStrategy import SporeStrategy
from game_message import Spore, TeamGameState, SporeMoveAction, Position, SporeSplitAction
from Utils import get_enemy_position_dict

DIRS = [Position(0, -1), Position(0, 1), Position(-1, 0), Position(1, 0)]

class ExpansionSporeStrategy(SporeStrategy):
    visited_positions = set()

    def __init__(self):
        super().__init__()
        self.last_pos = None
        self.current_pos = None
        self.current_targets = []

    def set_current_targets(self, targets):
        self.current_targets = targets

    def get_action(self, spore: Spore, game_message: TeamGameState):
        world = game_message.world
        game_map = world.map
        my_team_id = game_message.yourTeamId
        ExpansionSporeStrategy.visited_positions.add((spore.position.x, spore.position.y))
        max_score = -float('inf')
        best_direction = None
        enemies_dict = get_enemy_position_dict(world, my_team_id)

        for d in DIRS:
            nx, ny = spore.position.x + d.x, spore.position.y + d.y
            if 0 <= nx < game_map.width and 0 <= ny < game_map.height:
                score = 0
                owner = world.ownershipGrid[nx][ny]
                biomass = world.biomassGrid[nx][ny]
                #expansion
                if (nx, ny) not in ExpansionSporeStrategy.visited_positions:
                    score += 100
                else:
                    score -= 30

                #priorité au terrain vide
                if biomass == 0:
                    score += 50

                #bonus si c'est un zone des mechants ennemis
                if owner != my_team_id and owner != game_message.constants.neutralTeamId:
                    score += 30
                
                #si c'est notre propre biomasse--
                if owner == my_team_id:
                    score -= 60

                # évitement ennemis plus forts que nous
                enemy = enemies_dict.get((nx, ny))
                if enemy:
                    if enemy.biomass < spore.biomass:
                        score += 40
                    else:
                        score -= 500

                #éviter les cases déjà ciblées
                for target in self.current_targets:
                    if target.x == nx and target.y == ny:
                        score -= 50

                #ne pas reculer
                if self.last_pos and nx == self.last_pos.x and ny == self.last_pos.y:
                    score -= 150

                if score > max_score:
                    max_score = score
                    best_direction = d

        if best_direction:
            self.last_pos = spore.position
            if spore.biomass >= 6:
                return SporeSplitAction(spore.id, spore.biomass // 2, best_direction)
            return SporeMoveAction(spore.id, best_direction)

        return None
