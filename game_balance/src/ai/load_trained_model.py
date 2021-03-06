from glob import escape
import logging
from functools import partial
from multiprocessing import Pool

import numpy as np
import pandas as pd
import ray
import tensorflow as tf
from gym import Env
from gym.spaces import Box
from ray.rllib.agents.ppo import PPOTrainer

from game_balance.src.environment.game import play_a_game
from game_balance.src.environment.weapons import define_weapons

logger = logging.getLogger(__name__)

games_per_episode = 250

class HuntEnv(Env):
    # made with the help of:
    # https://www.youtube.com/watch?v=bD6V3rcr_54
    # https://github.com/ray-project/ray/blob/master/rllib/examples/custom_env.py
    def __init__(self, config):  # config only due to rllib requirements; won't use it here
        self.action_space = Box(low=np.array([-1]*12), high=np.array([1]*12))  # tweaks to damage and range of weapons
        self.observation_space = Box(low=np.array([0]*6), high=np.array([1]*6))  # winrates of particular weapons

        available_weapons = define_weapons()
        multip_pool = Pool()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(games_per_episode))
        state, _ = evaluate_game_result(result)
        self.state = state
        self.steps_counter = 0
        self.weapons_stats = [("Winfield M1873 Talon", 110, 95, 150, 16, 20), ("Romero", 200, 15, 54, 1, 12),
                              ("Caldwell Pax", 110, 86, 31, 6, 12), ("Lebel 1886", 132, 250, 54, 10, 5),
                              ("Sparks LRR", 149, 344, 54, 1, 16), ("Specter 1882 Bayonet", 175, 10, 168, 5, 10)
                              ]

    def step(self, action):
        self.steps_counter += 1
        # action is like: [-0.62, -0.64, -0.72, 0.53, -0.6, -0.38, 0.59, 0.21, -0.25, 0.04, -0.17, 0.69]
        # which translates to something like: [120, 12, 200, 15, 100, 80, 130, 200, 149, 300, 165, 10]
        weapons_stats = modify_weapons(weapons_stats=self.weapons_stats, action=action)
        print(weapons_stats)
        available_weapons = define_weapons(*weapons_stats)
        multip_pool = Pool()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(games_per_episode))
        state, reward = evaluate_game_result(result)
        self.state = state
        done = True
        info = {}
        if self.steps_counter == 100: 
            print(f"Current reward: {reward}")
            print(f"Winrates (state) presents itself as follows: {state}")
            for weapon in available_weapons:
                print(f"Name: {weapon.name}, dmg: {weapon.damage}, range: {weapon.effective_range}")
            print("----------------------------------------------------------")
            self.steps_counter = 0

        return self.state, reward, done, info

    def render(self):
        # Only for visualization purposes, omitted in this project
        pass

    def reset(self):
        available_weapons = define_weapons()
        multip_pool = Pool()
        result = multip_pool.map(partial(play_a_game, available_weapons=available_weapons), range(games_per_episode))
        state, _ = evaluate_game_result(result)
        self.state = state
        return self.state


def modify_weapons(weapons_stats, action):
    # example weapon_stats[0] input value: ("Winfield M1873 Talon", 110, 95, 150, 16, 20)
    modified_weapons = []
    for wep_id, weapon in enumerate(weapons_stats):
        new_dmg = action_to_value(action[wep_id*2], all_constraints[wep_id][1])
        new_range = action_to_value(action[wep_id*2+1], all_constraints[wep_id][2])
        modified_weapons.append((weapon[0], new_dmg, new_range, *weapon[3:]))
    return modified_weapons


def action_to_value(action, constraints):
    """converts action, which is a number between -1 and 1 into a natural number from a given value range"""
    try:
        result = round(action * (constraints[1]-constraints[0])/2 + (constraints[1]+constraints[0])/2)
    except ValueError:
        logger.warning(f"Nan action! Action: {action}, constraints:{constraints}")
        result = (constraints[1]-constraints[0])/2
    return result


# name, damage, range, melee_dmg, mag_ammo, ammo_supply
winfield_constraints = ("Winfield M1873 Talon", (80, 130), (60, 120), 150, 16, 20)
romero_constraints = ("Romero", (150, 225), (10, 20), 54, 1, 12)
pax_constraints = ("Caldwell Pax", (80, 115), (60, 100), 31, 6, 12)
lebel_constraints = ("Lebel 1886", (110, 145), (180, 300), 54, 10, 5)
sparks_constraints = ("Sparks LRR", (130, 149), (250, 400), 54, 1, 16)
specter_constraints = ("Specter 1882 Bayonet", (150, 200), (8, 15), 168, 5, 10)

all_constraints = [winfield_constraints, romero_constraints, pax_constraints,
                   lebel_constraints, sparks_constraints, specter_constraints]



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

    state = df_plot_data["Winrate"].fillna(0)
    df_plot_data["Winrate_deviation"] = abs(df_plot_data["Winrate"] - 0.5)
    reward = 3 - df_plot_data["Winrate_deviation"].sum()  # 3 = 6*0.5; there are 6 weapons, max deviation is 0.5
    state = list(state)
    return state, reward

if __name__ == "__main__":
    how_many_gpus = len(tf.config.list_physical_devices('GPU'))
    ray.init(num_gpus=how_many_gpus)

    config = {
        # Env class to use (here: gym.Env sub-class from above).
        "env": HuntEnv,
        "rollout_fragment_length": 128,
        "train_batch_size": 128,
        "num_gpus": how_many_gpus,
        "num_gpus_per_worker": how_many_gpus,
        "framework": "tf",
        "create_env_on_driver": True,
        # Parallelize environment rollouts.
        "num_workers": 1,
    }
    trainer = PPOTrainer(config=config, env=HuntEnv)


    trainer.load_checkpoint("C:/Users/Jacek/Desktop/magisterka_model/checkpoint-211")

    env = HuntEnv(config=config)
    try:
        action = trainer.compute_single_action(observation = env.observation_space.sample())
        print(action)
        state, reward, done, info = env.step(action)
        print(state)
        print(reward)
    except Exception as e:
        print(e)
