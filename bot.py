import game_message
from GenerativeSporeStrategy import GenerativeSporeStrategy
from SpawnerStrategy import SpawnerStrategy
from SporeStrategy import SporeStrategy
from game_message import *

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        spore_strategies = [str, SporeStrategy]
        spawner_strategies = [str, SpawnerStrategy]

    def get_next_move(self, game_message: TeamGameState) -> list[Action]:
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)

        actions = []

        my_team: TeamInfo = game_message.world.teamInfos[game_message.yourTeamId]
        if len(my_team.spawners) == 0:
            actions.append(SporeCreateSpawnerAction(sporeId=my_team.spores[0].id))

        elif len(my_team.spores) == 0:
            actions.append(
                SpawnerProduceSporeAction(spawnerId=my_team.spawners[0].id, biomass=20)
            )

        else:
            actions.append(
                SporeMoveToAction(
                    sporeId=my_team.spores[0].id,
                    position=Position(
                        x=random.randint(0, game_message.world.map.width - 1),
                        y=random.randint(0, game_message.world.map.height - 1),
                    ),
                )
            )

        # You can clearly do better than the random actions above. Have fun!!
        """
        actions = run_strategies(game_message)
        return actions


def create_spore_strategy(spore, game_message) -> SporeStrategy:
    return GenerativeSporeStrategy()


def create_spawner_strategy(spawner, game_message) -> SpawnerStrategy:
    pass


def run_strategies(bot, game_message: TeamGameState):
    actions = []
    team_info = game_message.world.teamInfos[game_message.yourTeamId]
    if not bot.spore_strategies.keys:
        bot.spore_strategies = dict.fromKeys(team_info.spawners, create_spore_strategy)
    if not bot.spawner_strategies.keys:
        bot.spawner_strategies = dict.fromkeys(team_info.spawners, create_spawner_strategy)
    for spore in team_info.spores:
        if bot.spore_strategies[spore.id] is None:
            sporeStrategy = create_spore_strategy(spore, game_message)
            actions.append(sporeStrategy.get_action(spore,game_message))
    for spawner in team_info.spawners:
        if bot.spawner_strategies[spawner.id] is None:
            spawnerStrategy = create_spawner_strategy(spawner,game_message)
            actions.append(spawnerStrategy.get_action(spawner,game_message))
    return actions
