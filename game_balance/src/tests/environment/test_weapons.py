import pytest
from src.environment.weapons import Weapon, define_weapons

weapons = define_weapons()

@pytest.mark.parametrize("weapon", weapons)
def test_weapon_dealing_damage(weapon):
    # make sure we don't run out of ammo
    weapon.ammo_loaded = 10_000

    # Check obvious full dmg up to effective range 
    # and 0 damage when at or over 2*effective range
    assert weapon.deal_damage(0) == weapon.damage
    assert weapon.deal_damage(weapon.effective_range/2) == weapon.damage
    assert weapon.deal_damage(weapon.effective_range/4) == weapon.damage
    assert weapon.deal_damage(weapon.effective_range*3/4) == weapon.damage
    assert weapon.deal_damage(weapon.effective_range) == weapon.damage
    assert weapon.deal_damage(2*weapon.effective_range) == 0
    assert weapon.deal_damage(2*weapon.effective_range+1) == 0
    assert weapon.deal_damage(3*weapon.effective_range) == 0 

    # Check if damage between 1 effective and 2 effective ranges are below a line and in descending order
    # Maybe there is a better way to test a parabola, but this is good enough for now
    dmgs_in_parabola = []
    for i in range(weapon.effective_range, weapon.effective_range*2, 3):
        new_dmg = weapon.deal_damage(i)
        dmgs_in_parabola.append(new_dmg)
        assert new_dmg >= -(weapon.damage/weapon.effective_range)*i + 2*weapon.damage
    assert all(earlier >= later for earlier, later in zip(dmgs_in_parabola, dmgs_in_parabola[1:]))
    