import logging
from random import seed
from csv import writer
from multiprocessing import Pool
from gym import Env
from gym.spaces import Box
from functools import partial

import pandas as pd

from game_balance.src.environment.game import play_a_game
from game_balance.src.environment.weapons import define_weapons
import pandas as np

logger = logging.getLogger(__name__)

seed(8247)  # for reproducibility


class GameEnv(Env):
    # https://www.youtube.com/watch?v=bD6V3rcr_54
    # https://github.com/ray-project/ray/blob/master/rllib/examples/custom_env.py
    def __init__(self):
        self.action_space = Box(np.array([-1]*12), np.array([1]*12))  # tweaks to damage and range of weapons
        self.observation_space = Box(np.array([0]*6), np.array([1]*6))  # winrates of particular weapons

        available_weapons = define_weapons()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(1_000))
        state, reward = evaluate_game_result(result)
        self.state = state

    def step(self, action):
        pass

    def render(self):
        pass

    def reset(self):
        pass


def action_to_value(action, constraints):
    """converts action, which is a number between -1 and 1 into a natural number from a given value range"""
    return round(action * (constraints[1]-constraints[0])/2 + (constraints[1]+constraints[0])/2)


# damage, range, melee_dmg, mag_ammo, ammo_supply
winfield_constraints = ((80, 130), (60, 120), 150, 16, 20)
romero_constraints = ((150, 225), (10, 20), 54, 1, 12)
pax_constraints = ((80, 115), (60, 100), 31, 6, 12)
lebel_constraints = ((110, 145), (180, 300), 54, 10, 5)
sparks_constraints = ((130, 149), (250, 400), 54, 1, 16)
specter_constraints = ((150, 200), (8, 15), 168, 5, 10)


def run_experiment():
    # initial weapon characteristics
    winfield_stats = ("Winfield M1873 Talon", 110, 95, 150, 16, 20)
    romero_stats = ("Romero", 200, 15, 54, 1, 12)
    pax_stats = ("Caldwell Pax", 110, 86, 31, 6, 12)
    lebel_stats = ("Lebel 1886", 132, 250, 54, 10, 5)
    sparks_stats = ("Sparks LRR", 149, 344, 54, 1, 16)
    specter_stats = ("Specter 1882 Bayonet", 175, 10, 168, 5, 10)

    available_weapons = define_weapons()


def evaluate_game_result(games_data):
    df_game_data = pd.DataFrame(games_data, columns=["Id", "Weapon0", "Weapon1"])

    df_game_data = df_game_data.reindex(df_game_data.loc[:, "Id"]).drop("Id", axis=1)

    df_game_data.loc[:, :] = df_game_data.loc[df_game_data["Weapon0"] != df_game_data["Weapon1"], :]
    df_plot_data = pd.DataFrame([[0] * 3] * 6, index=["Winfield M1873 Talon", "Romero", "Caldwell Pax",
                                                      "Lebel 1886", "Sparks LRR", "Specter 1882 Bayonet"],
                                columns=["Games", "Wins", "Winrate"])
    grp0 = df_game_data.groupby("Weapon0")
    grp1 = df_game_data.groupby("Weapon1")

    df_plot_data = df_plot_data.join(grp0.count().loc[:, "Weapon1"]).join(grp1.count().loc[:, "Weapon0"]).fillna(0)
    df_plot_data["Games"] = df_plot_data["Weapon1"] + df_plot_data["Weapon0"]
    df_plot_data["Wins"] = df_plot_data["Weapon1"]
    df_plot_data["Winrate"] = df_plot_data["Wins"] / df_plot_data["Games"]
    df_plot_data = df_plot_data.drop("Weapon0", axis=1).drop("Weapon1", axis=1)

    state = df_plot_data["Winrate"]
    df_plot_data["Winrate_deviation"] = abs(df_plot_data["Winrate"] - 0.5)
    reward = 3 - df_plot_data["Winrate_deviation"].sum()  # 3 = 6*0.5; there are 6 weapons, max deviation is 0.5
    return state, reward


if __name__ == "__main__":
    with open("../../game_data.csv", mode="w", newline='') as file:
        writer = writer(file)
        header = ["Id", "Weapon0", "Weapon1"]
        writer.writerow(header)
        multip_pool = Pool()
        available_weapons = define_weapons()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(100))
        state, reward = evaluate_game_result(result)
        writer.writerows(result)

