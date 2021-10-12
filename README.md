# masters_thesis

Repository including all of the mini-project's that will be a part of my master's thesis. The idea is to find unusual AI/ML applications and implement them. The collective of this work will later be summarised in my Master's Thesis

Each project contains its own README.md, to learn about each project go to a proper directory and read about it there

Main thesis idea: Reinforcement learning is widely researched yet very little business applications exist. Various project presented in the thesis serve as a way of exploring the possiblities of well known ML algorithms with the idea of discovering new business applications for RL and whole of ML.

## Ideas for projects:

- Solving monopoly with RL
- Sorting an array with ML [ADA sort paper](https://www.researchgate.net/publication/305362015_AdaSort_Adaptive_Sorting_using_Machine_Learning), [So called "ML Sort"](https://arxiv.org/abs/1805.04272)
- Generating human faces with OLS - [reddit inspiration](https://www.reddit.com/r/learnmachinelearning/comments/npojso/built_linear_regression_model_which_can_predict/?utm_medium=android_app&utm_source=share) and a [similar post](https://www.reddit.com/r/artificial/comments/ozsdju/generate_new_images_from_any_userbased_inputs_say/?utm_medium=android_app&utm_source=share)
- Facial features recognition, eye color with k-means, age etc. TODO: find dataset.
- Regression and clustering with RL
- Clustering with varied feature weights. Check if exists within unsipervised learning, implent both in unsupervised and in RL?
- **Game balancing with AI/ML. Idea - build a simple "skirmish" game and balance it with AI. Tweaking game params based on performance. (IN PROGRESS)**
- Solve "Upgraded tic-tac-toe": https://youtu.be/bxXH5Q4ZUAw
- Do something similar to [Noncom exploit from 2b2t](https://github.com/nerdsinspace/nocom-explanation/blob/main/README.md)
- Enriching datasets with handmade examples based on domain knowledge. It's a way of introducing a priori knowledge to models. For example if we know that low income means someone is less likely to have a good credit score we include observations that follow this. Or in RL if we're certain that for a certain state we want a given action we create a number of identical observations indicating that, similarly to bootstrapping with immitation learning
- Reccomendation system based on RL (music with length of track played as reward)

## Inspirations:
https://bdtechtalks.com/2021/10/04/ea-reinforcement-learning-game-testing/
https://arxiv.org/abs/2106.12142 - new imitation learning SOTA algorithm - IQ-learning
