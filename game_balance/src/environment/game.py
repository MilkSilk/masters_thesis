import logging
from random import randint, seed
from csv import writer
from multiprocessing import Pool
from game_balance.src.environment.characters import Player
from game_balance.src.environment.weapons import get_random_weapon, define_weapons
from functools import partial

logging.basicConfig(filename='game.log', level=logging.DEBUG, filemode="w")
logger = logging.getLogger(__name__)

seed(8247)  # for reproducibility


class Game:
    """Class responsible for starting a duel between two players and determining the outcome"""
    def __init__(self, player0: Player, player1: Player):
        self.player0 = player0
        self.player1 = player1
        player0.add_target(player1)
        player1.add_target(player0)

    # First each player takes an action, then if there are enemy NPCs they take actions
    # After each action check if anyone has died
    def next_round(self):
        self.player0.take_action()
        if self.player1.health <= 0:
            logging.debug(str(self.player1) + " is dead!")
            return str(self.player0) + "(player 1) has killed " + str(self.player1)

        self.player1.take_action()
        if self.player0.health <= 0:
            logger.debug(str(self.player0) + " is dead!")
            return str(self.player1) + "(player 2) has killed " + str(self.player0)

        if randint(1, 5) == 5 and not self.player0.npc_enemy:
            self.player0.add_npc()
        if randint(1, 5) == 5 and not self.player1.npc_enemy:
            self.player1.add_npc()

        if self.player0.npc_enemy:
            self.player0.npc_enemy.take_action()
        if self.player1.npc_enemy:
            self.player1.npc_enemy.take_action()


def play_a_game(i, available_weapons):
    hunter_distance = randint(25, 300)
    player0 = Player("Dzejms", get_random_weapon(available_weapons), hunter_distance)
    player1 = Player("Emmmmmmmma", get_random_weapon(available_weapons), hunter_distance)
    game = Game(player0, player1)
    logger.debug(f'Hunters are {hunter_distance}m away from each other')
    for j in range(1000):
        round_outcome = game.next_round()
        if round_outcome:
            winner = int(round_outcome[round_outcome.find(')') - 1]) - 1
            break
    if winner:
        winners_weapon = player1.weapon.name
        losers_weapon = player0.weapon.name
    else:
        winners_weapon = player0.weapon.name
        losers_weapon = player1.weapon.name

    result = [i, winners_weapon, losers_weapon]
    return result


if __name__ == "__main__":
    with open("../../game_data.csv", mode="w", newline='') as file:
        writer = writer(file)
        header = ["Id", "Weapon0", "Weapon1"]
        writer.writerow(header)

        available_weapons = define_weapons()

        multip_pool = Pool()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(10_000))

        writer.writerows(result)



