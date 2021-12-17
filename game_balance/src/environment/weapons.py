from random import choice
import logging

logger = logging.getLogger(__name__)


class Weapon:
    """Represents a weapon, which can be used by a player in a fight"""

    def __init__(self, name, damage, effective_range,
                 melee_dmg, max_ammo, ammo_stock):
        self.name = name

        # stats from in-game GUI
        self.damage = damage
        self.effective_range = effective_range
        self.melee_dmg = melee_dmg

        # ammo attributes
        self.max_ammo = max_ammo
        self.ammo_loaded = self.max_ammo
        self.ammo_stock = ammo_stock

    def __str__(self):
        return str(self.name)

    def reload(self):
        logger.debug(str(self)+" is being reloaded")
        needed_ammo = self.max_ammo - self.ammo_loaded
        ammo_available = max(needed_ammo, self.ammo_stock)
        self.ammo_loaded += ammo_available
        self.ammo_stock -= ammo_available

    def deal_damage(self, distance):
        if self.ammo_loaded > 0:
            self.ammo_loaded -= 1
            if distance <= self.effective_range:
                return self.damage
            else:
                return max(-(1 / self.damage) * (distance - self.damage) ** 2 + self.damage, 0)
        else:
            raise NoAmmoException(message=self.name+" has no bullets in the chamber!")


class NoAmmoException(Exception):
    """Exception raised if player wants to shoot but they have no ammo"""

    def __init__(self, message="Your weapon has no bullets in it!"):
        self.message = message
        super().__init__(self.message)


def get_random_weapon():
    winfield = Weapon("Winfield M1873 Talon", 110, 95, 150, 16, 20)
    romero = Weapon("Romero", 200, 15, 54, 1, 12)
    pax = Weapon("Caldwell Pax", 110, 86, 31, 6, 12)
    lebel = Weapon("Lebel 1886", 132, 250, 54, 10, 5)
    sparks = Weapon("Sparks LRR", 149, 344, 54, 1, 16)
    specter = Weapon("Specter 1882 Bayonet", 175, 10, 168, 5, 10)
    available_weapons = [winfield, romero, pax, lebel, sparks, specter]
    chosen_weapon = choice(available_weapons)
    logger.debug(f'Getting a random weapon: {chosen_weapon.name}')
    return chosen_weapon
