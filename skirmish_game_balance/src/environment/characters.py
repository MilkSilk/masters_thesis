from random import randint
from weapons import NoAmmoException


class Character:
    """Abstract class for Player and NpcEnemy classes"""

    def __str__(self):
        return self.name

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return str(Character)+" has died."

    def approach_enemy(self):
        self.distance -= min(self.distance, self.speed)


class Player(Character):
    """
    The Player class takes decisions during a fight and stores weapons.

    Players could be also trained using AI to learn taking the best decisions,
    but what the code focuses on is tweaking weapon properties for game balance
    despite players playing suboptimally as it is usual in gaming.

    Actions which can be taken:

    - Shoot a weapon
    - Reload a weapon
    - Fight off NPC enemy
    - change distance from enemy

    """

    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 150
        self.distance = 300  # To enemy hunter, in meters
        self.speed = 25

    def shoot(self, distance):
        try:
            self.weapon.fire()
            return self.weapon.deal_damage(distance)
        except NoAmmoException:
            return 0

    def reload(self):
        self.weapon.reload()

    def fight_npc(self):
        return self.weapon.melee_dmg


class NpcEnemy(Character):
    """
    Abstract class describing enemies steered by the game, not other players.
    Zombie, Armored and Hellhound classes will inherit this.
    """

    def __init__(self, target):
        self.name = "NpcEnemy"+str(randint(1, 1000))
        self.health = 100
        self.damage = 20
        self.speed = 25  # Meters per round (round is ~ 5 sec, 25 is 5 sec times 5m/s, which is avg human run speed)
        self.target = target
        self.distance = randint(50, 200)

    def attack_hunter(self):
        self.target.take_damage()

    def take_action(self):
        if self.distance == 0:
            self.attack_hunter()
        else:
            self.approach_enemy()
