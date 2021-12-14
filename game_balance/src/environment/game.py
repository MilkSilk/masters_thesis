import logging
from random import randint
from game_balance.src.environment.characters import Player
from game_balance.src.environment.weapons import get_random_weapon

logging.basicConfig(filename='game.log', level=logging.DEBUG, filemode="w")
logger = logging.getLogger(__name__)


class Game:
    """Class responsible for starting a duel between two players and determining the outcome"""
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        player1.add_target(player2)
        player2.add_target(player1)

    # First each player takes an action, then if there are enemy NPCs they take actions
    # After each action check if anyone has died
    def next_round(self):
        self.player1.take_action()
        if self.player2.health <= 0:
            logging.debug(str(self.player2)+" is dead!")
            return str(self.player1)+" has killed "+str(self.player2)

        self.player2.take_action()
        if self.player1.health <= 0:
            logger.debug(str(self.player1)+" is dead!")
            return str(self.player2)+" has killed "+str(self.player1)

        if randint(1, 5) == 5 and not self.player1.npc_enemy:
            self.player1.add_npc()
        if randint(1, 5) == 5 and not self.player2.npc_enemy:
            self.player2.add_npc()

        if self.player1.npc_enemy:
            self.player1.npc_enemy.take_action()
        if self.player2.npc_enemy:
            self.player2.npc_enemy.take_action()


if __name__ == "__main__":
    for j in range(100):
        player1 = Player("Dzejms", get_random_weapon())
        player2 = Player("Emmmmmmmma", get_random_weapon())
        game = Game(player1, player2)
        logger.debug(f'Hunters are {player1.distance}m away from each other')
        for i in range(100):
            round_outcome = game.next_round()
            if round_outcome:
                print(round_outcome)
                break

