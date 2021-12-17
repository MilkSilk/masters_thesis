from random import randint, choice, getrandbits
from game_balance.src.environment.weapons import NoAmmoException
import logging

logger = logging.getLogger(__name__)


class Character:
    """Abstract class for Player and NpcEnemy classes"""
    def __init__(self):
        self.name = ""
        self.health = 100
        self.distance = 100
        self.speed = 25
        self.target = None

    def __str__(self):
        return str(self.name)

    def take_damage(self, damage):
        logger.debug(str(self)+f' takes {str(damage)} damage!')
        self.health -= damage
        if self.health <= 0:
            logger.debug(str(self)+" dies!")
            return str(Character)+" has died."

    def approach_enemy(self):
        self.distance -= min(self.distance, self.speed)
        logger.debug(f'{self.name} approaches {self.target.name}, they are {self.distance}m away')


class Player(Character):
    """
    The Player class takes decisions during a fight and stores weapons.

    Players could be also trained using AI to learn taking the best decisions,
    but what the code focuses on is tweaking weapon properties for game balance
    despite players playing suboptimally as it is usual in gaming.

    Actions which can be taken:

    - Shoot a weapon at human opponent
    - Reload a weapon
    - Fight off NPC enemy
    - Approach the human opponent

    """

    def __init__(self, name, weapon, distance=300):
        super().__init__()
        self.name = name
        self.weapon = weapon
        self.distance = distance  # To enemy hunter, in meters
        self.damage_modifiers = {"leg": 0.3, "arm": 0.7, "torso": 1, "head": 2}
        self.health = 150
        self.speed = 25
        self.target = None
        self.npc_enemy: NpcEnemy = None
        logger.debug("New hunter called "+str(self)+" enters the bayou")

    def add_target(self, target):
        self.target = target

    def shoot(self):
        logger.debug(str(self)+" shoots their "+str(self.weapon))
        try:
            dmg_modifier = choice([x for x in self.damage_modifiers.items()])
            logger.debug(f'It\'s a shot to the {dmg_modifier[0]}')
            dmg_modifier = dmg_modifier[1]
            damage_dealt = self.weapon.deal_damage(self.distance) * dmg_modifier
            self.target.take_damage(damage_dealt)
            return
        except NoAmmoException:
            logger.critical(str(self) + " shot their weapon ("
                            + str(self.weapon) + ") without any ammo!")
            return 0

    def reload(self):
        logger.debug(str(self)+" reloaded their weapon")
        self.weapon.reload()

    def fight_npc(self):
        if self.npc_enemy.take_damage(self.weapon.melee_dmg):
            logger.debug(str(self)+" killed an NPC")
            self.npc_enemy = None

    def take_action(self):
        # If enemy NPC is next to us we attack it
        if self.npc_enemy and self.npc_enemy.distance == 0:
            logger.debug(str(self)+" attacks the enemy NPC")
            self.fight_npc()
        # If we don't have ammo we reload
        elif self.weapon.ammo_loaded == 0:
            logger.debug(str(self)+" reloads their weapon ("+str(self.weapon)+")")
            self.reload()
        # If enemy is more than 2 effective ranges away we approach them
        # If enemy is between 2 effective ranges and 1 effective range we 50% shoot 50% approach
        # (bool(getrandbits(1)) is 50% True, 50% False
        # If enemy is within effective range we shoot
        elif self.distance > 2*self.weapon.effective_range or \
                (bool(getrandbits(1)) and self.distance > self.weapon.effective_range):
            self.approach_enemy()
            self.target.distance -= min(self.distance, self.speed)
        else:
            return self.shoot()
        return

    def add_npc(self):
        npc_enemy = get_random_npc(self)
        logger.debug(str(self)+f' has been added a new NPC enemy {npc_enemy.name}, which is '
                               f'{npc_enemy.distance}m away')
        self.npc_enemy = npc_enemy


class NpcEnemy(Character):
    """
    Abstract class describing enemies steered by the game, not other players.
    Zombie, Armored and Hellhound classes will inherit this.
    """

    def __init__(self, target):
        super().__init__()
        self.name = "NpcEnemy"+str(randint(1, 1000))
        self.health = 100
        self.damage = 20
        self.speed = 25  # Meters per round (round is ~ 5 sec, 25 is 5 sec times 5m/s, which is avg human run speed)
        self.target = target
        self.distance = randint(10, 100)

    def attack_hunter(self):
        logger.debug(str(self)+" attacks "+str(self.target))
        self.target.take_damage(self.damage)

    def take_action(self):
        if self.distance == 0:
            self.attack_hunter()
        else:
            self.approach_enemy()


class Zombie(NpcEnemy):
    """
    The zombie enemy, has stats same as base NpcEnemy
    """

    def __init__(self, target):
        super().__init__(target)
        self.name = "Zombie"+str(randint(1, 1000))


class Armored(NpcEnemy):
    """
    Armored enemy class - stronger than a zombie health and damage-wise but slower
    """

    def __init__(self, target):
        super().__init__(target)
        self.name = "Armored"+str(randint(1, 1000))
        self.health = 150
        self.damage = 40
        self.speed = 10  # Meters per round (round is ~ 5 sec, 25 is 5 sec times 5m/s, which is avg human run speed)


class Hellhound(NpcEnemy):
    """
    Hellhound class - a hero with less health than a zombie but a bit more damage and much more speed
    """

    def __init__(self, target):
        super().__init__(target)
        self.name = "Hellhound"+str(randint(1, 1000))
        self.health = 80
        self.damage = 30
        self.speed = 50  # Meters per round (round is ~ 5 sec, 25 is 5 sec times 5m/s, which is avg human run speed)


def get_random_npc(target):
    logger.debug("Getting a random NPC enemy")
    zombie = Zombie(target)
    armored = Armored(target)
    hellhound = Hellhound(target)
    available_npc = [zombie, armored, hellhound]
    return choice(available_npc)
