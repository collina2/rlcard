''' An example of evluating the trained models in RLCard
'''
import os
import argparse

import sys

sys.path.insert(1, '../')



import rlcard
from rlcard import models
print(rlcard)
from rlcard.agents import (
    DQNAgent,
    NFSPAgent
)

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    else:  # A model in the model zoo
        from rlcard import models
        agent = models.load(model_path).agents[position]
    
    return agent

def evaluate(args):

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make(args.env, config={'seed': args.seed})

    # Load models
    agents = []
    for position, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)

    # Evaluate
    games_won = [0, 0, 0]
    rewards = tournament(env, args.num_games, games_won)
    model_names = ["New DQN", "Old DQN", "Random "]
    for position, reward in enumerate(rewards):
        print("Model:", model_names[position], "| Avg Reward:", format(reward, '.3f'), "| Win Rate:", str(format(games_won[position] / args.num_games * 100, '.2f')) + "%")

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument(
        '--env',
        type=str,
        default='uno',
        choices=[
            'uno',
        ],
    )
    parser.add_argument(
        '--models',
        nargs='*',
        default=[
            'experiments/DQN Custom Rewards/model.pth',
            'experiments/DQN Basic Rewards/model.pth',
            'random',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=47,
    )

    parser.add_argument(
        '--num_games',
        type=int,
        default=10,
    )
     

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    evaluate(args)

