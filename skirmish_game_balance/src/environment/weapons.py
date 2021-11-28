class Weapon:
    """Represents a weapon, which can be used by a player in a fight"""

    def __init__(self, name, damage, effective_range, reload_speed,
                 melee_dmg, max_ammo, max_ammo_stock):
        self.name = name

        # stats from in-game GUI
        self.damage = damage
        self.effective_range = effective_range
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

    def fire(self):
        if self.ammo_loaded > 0:
            self.ammo_loaded -= 1
            return "Action performed"
        else:
            raise NoAmmoException(message=self.name+" has no bullets in the chamber!")

    def deal_damage(self, distance):
        if distance <= self.effective_range:
            return self.damage
        else:
            return -(1/self.damage) * (distance-self.damage) ** 2 + self.damage


class NoAmmoException(Exception):
    """Exception raised if player wants to shoot but they have no ammo"""

    def __init__(self, message="Your weapon has no bullets in it!"):
        self.message = message
        super().__init__(self.message)