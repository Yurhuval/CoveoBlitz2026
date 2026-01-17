from abc import ABC, abstractmethod

from Strategy import Strategy
from game_message import TeamGameState, Spore, Position


class SporeStrategy(Strategy):
    def __init__(self, target = None):
        super().__init__()
        self.target : Position = target
        self.path = list[Position]()
        self.target = None
    @abstractmethod
    def get_action(self,spore : Spore, game_message : TeamGameState):
        pass


    def pathFindinding(self,current : Position, target : Position,game_message : TeamGameState) -> list[Position]:
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, current)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, target)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                # Get node position
                node_position = Position(current_node.position.x + new_position[0], current_node.position.y + new_position[1])

                if game_message.world.map.width > node_position.x >= 0 and node_position.y < game_message.world.map.height and node_position.y >= 0:
                    new_node = Node(current_node, node_position)

                    children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                if child in closed_list:
                    continue

                # Create the f, g, and h values
                if game_message.world.ownershipGrid[child.position.x][child.position.y] == game_message.yourTeamId:
                    child.g = current_node.g
                else :
                    child.g = current_node.g + game_message.world.biomassGrid[child.position.x][child.position.y] + 1
                child.h = ((child.position.x - end_node.position.x) ** 2) + (
                            (child.position.y - end_node.position.y) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                skip_child = False
                for open_node in open_list:
                    if child == open_node and child.g >= open_node.g:
                        skip_child = True
                        break

                if skip_child:
                    continue

                # Add the child to the open list
                open_list.append(child)
    def calculatePath(self,current, target,game_message : TeamGameState):
        if self.path is None:
            self.path = self.pathFindinding(current,target,game_message)
            self.target = target
        else :
            self.path = self.path[self.path.index(current):]
    def recalculate_path(self,current, target,game_message : TeamGameState):
        self.path = self.pathFindinding(current,target,game_message)
        self.target = target
    def next_step(self,current):
        try:
            return self.path[self.path.index(current)+1]
        except IndexError:
            return None
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position




