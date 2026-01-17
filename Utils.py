from game_message import Position


def get_distance(position1:Position, position2: Position):
    return abs(position1.x - position2.x) + abs(position1.y - position2.y)

def get_enemy_position_dict(world, my_team_id):

    mechants = {}
    for spore in world.spores:
        if spore.teamId != my_team_id:
            mechants[(spore.position.x, spore.position.y)] = spore
    return mechants