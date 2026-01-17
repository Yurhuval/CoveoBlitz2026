from game_message import Position


def get_distance(position1:Position, position2: Position):
    return abs(position1.x - position2.x) + abs(position1.y - position2.y)