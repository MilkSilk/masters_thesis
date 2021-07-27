# Balancing a simple game with AI
This project's purpose is to show how modern AI algorithms can offer
insight to game developers regarding the balance of their games for
better UX. 

Apart from demonstrating the above, a number of approaches will
be presented to illustrate how the algorithms one would expect the
least can also serve as a tool for game balancing.

The code bases upon [Hunt: Showdown](https://www.huntshowdown.com/)
The only elements that will be inspired are: weapons, core mechanics
like gunfight, consumable items' utilization, 
tools available in-game. The gameplay details will be
omitted as this project's aim isn't to create a playable game but
instead show how AI can serve to balance a game.

The choice of this game isn't accidental as the author has experience
with it and follows the development of this game closely. The specifics
of how the developers at Crytek choose to balance the game are
multifaceted and go beyond what will be presented here.
This project aims to change the weapon, tools and consumables
parameters, where in real game additional balance mechanisms are at 
play such as: item price, audio cues, item unlock system etc.

## Code logic

The environment.py file contains code relevant to the game. It enables
to simulate duels between player groups, preparation of a player
for a game, weapon used by players for fighting others and similar.

In the AI module (/ai directory) a number of files can be found,
each of them employs a different strategy to balancing the game.

To run the project use the main.py script. It executes the balancing
process based upon given initial state. Initialization can be random,
based upon real weapon statistics for Hunt:Showdown, or can be user
defined.

## TODO:
- Implement the game itself
    - Create environment: fight/duel system, outcome evaluation etc.
    - Character/weapon objects which will be altered by AI for balance
- Create AIs 
    - RL solution (duh!)
    - Analysing OLS parameters, and automating game changes based on 
      the parameters (if a parameter is high then reduce stats of a
      given character/weapon)
    - Other uncommon solutions (clustering + analysing
      the worst and best performing clusters)
      
## Literature
https://www.aaai.org/Papers/AIIDE/2006/AIIDE06-005.pdf
http://www.cse.lehigh.edu/~munoz/Publications/IJCAI05W-proceedings.pdf#page=11
https://www.scitepress.org/Papers/2019/73954/73954.pdf

