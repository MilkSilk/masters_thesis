import logging
from random import randint


class Game:
    """Class responsible for starting a duel between two players and determining the outcome"""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    # First each player takes an action, then if there are enemy NPCs they take actions
    # After each action check if anyone has died
    def next_round(self):
        self.player1.take_action()
        if self.player2.health <= 0:
            logging.debug(str(self.player2)+" is dead!")
            return str(self.player1)+" has killed "+str(self.player2)
        self.player2.take_action()
        if self.player1.health <= 0:
            logging.debug(str(self.player1)+" is dead!")
            return str(self.player2)+" has killed "+str(self.player1)
        if randint(1, 5) == 5:
            self.player1.npc_enemy = NpcEnemy()
