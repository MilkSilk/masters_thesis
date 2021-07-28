class Game:
    pass


class Player:
    """
    The Player class takes decisions during a fight and stores weapons.

    Players could be also trained using AI to learn taking the best decisions,
    but what the code focuses on is tweaking weapon properties for game balance
    despite players playing suboptimally as it is usual in gaming.

    Actions which can be taken:

    - Shoot a weapon
    - Reload a weapon
    - Scavenge for ammo
    - Go into a better position
    - change distance from enemy

    """

    def __init__(self, primary_weapon, secondary_weapon):
        self.primary_weapon = primary_weapon
        self.secondary_weapon = secondary_weapon


class Weapon:
    """Represents a weapon, which can be used by a player in a fight"""

    def __init__(self, name, is_primary, damage, effective_range, rate_of_fire,
                 reload_speed, melee_dmg, max_ammo, max_ammo_stock):
        self.name = name
        self.is_primary = is_primary

        # stats from in-game GUI
        self.damage = damage
        self.effective_range = effective_range
        self.rate_of_fire = rate_of_fire
        self.reload_speed = reload_speed
        self.melee_dmg = melee_dmg

        # ammo attributes
        self.max_ammo = max_ammo
        self.ammo_loaded = self.max_ammo
        self.max_ammo_stock = max_ammo_stock
        self.ammo_stock = self.max_ammo_stock

    def reload(self):
        needed_ammo = self.max_ammo - self.ammo_loaded
        ammo_available = max(needed_ammo, self.ammo_stock)
        self.ammo_loaded += ammo_available
        self.ammo_stock -= ammo_available
        return "Action performed"

    def fire(self):
        if self.ammo_loaded > 0:
            self.ammo_loaded -= 1
            return "Action performed"
        else:
            raise NoAmmoException(message=self.name+" has no bullets in the chamber!")

    def scavenge_for_ammo(self):
        self.ammo_stock += int(self.max_ammo_stock/3)
        return "Action performed"


class NoAmmoException(Exception):
    """Exception raised if player wants to shoot but they have no ammo"""

    def __init__(self, message="Your weapon has no bullets in it!"):
        self.message = message
        super().__init__(self.message)


