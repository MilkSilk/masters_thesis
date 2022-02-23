import logging
from random import seed
from csv import writer
from multiprocessing import Pool

import pandas as pd

from game_balance.src.environment.game import play_a_game
from game_balance.src.environment.weapons import define_weapons
import pandas as np

logger = logging.getLogger(__name__)

seed(8247)  # for reproducibility

winfield_constraints = ((80, 130), (60, 120), 150, (12, 20), (10, 30))
romero_constraints = (200, 15, 54, 1, 12)
pax_constraints = (110, 86, 31, 6, 12)
lebel_constraints = (132, 250, 54, 10, 5)
sparks_constraints = (149, 344, 54, 1, 16)
specter_constraints = (175, 10, 168, 5, 10)


def run_experiment():
    # initial weapon characteristics
    winfield_stats = ("Winfield M1873 Talon", 110, 95, 150, 16, 20)
    romero_stats = ("Romero", 200, 15, 54, 1, 12)
    pax_stats = ("Caldwell Pax", 110, 86, 31, 6, 12)
    lebel_stats = ("Lebel 1886", 132, 250, 54, 10, 5)
    sparks_stats = ("Sparks LRR", 149, 344, 54, 1, 16)
    specter_stats = ("Specter 1882 Bayonet", 175, 10, 168, 5, 10)

    available_weapons = define_weapons()


def evaluate_game_fairness(games_data):
    df_game_data = pd.DataFrame(games_data, columns=["Id", "Weapon0", "Weapon1"])
    df_game_data = df_game_data.reindex(df_game_data.loc[:, "Id"]).drop("Id", axis=1)
    df_game_data.loc[:, :] = df_game_data.loc[df_game_data["Weapon0"] != df_game_data["Weapon1"], :]
    df_plot_data = pd.DataFrame()
    grp0 = df_game_data.groupby("Weapon0")
    grp1 = df_game_data.groupby("Weapon1")
    df_plot_data.loc[:, "Wins"] = grp0.count().loc[:, "Weapon1"]
    df_plot_data.loc[:, "Games"] = grp0.count().loc[:, "Weapon1"] + grp1.count().loc[:, "Weapon0"]
    df_plot_data.loc[:, "Winrate"] = df_plot_data.loc[:, "Wins"] / df_plot_data.loc[:, "Games"]
    df_plot_data["Winrate_deviation"] = abs(df_plot_data["Winrate"] - 0.5)
    reward = 3 - df_plot_data["Winrate_deviation"].sum()  # 3 = 6*0.5; there are 6 weapons, max deviation is 0.5
    return reward


if __name__ == "__main__":
    with open("../../game_data.csv", mode="w", newline='') as file:
        writer = writer(file)
        header = ["Id", "Weapon0", "Weapon1"]
        writer.writerow(header)
        multip_pool = Pool()
        result = multip_pool.map(play_a_game, range(10_000))  # sped up from 7.5 secs to 2.2 secs; instead of loop
        writer.writerows(result)

