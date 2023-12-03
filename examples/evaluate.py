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
    elif os.path.isdir(model_path):  # CFR model
        from rlcard.agents import CFRAgent
        agent = CFRAgent(env, model_path)
        agent.load()
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
    for position, reward in enumerate(rewards):
        print("Model:", args.models[position], "| Avg Reward:", reward, "| Win Rate:", str(games_won[position] / args.num_games * 100) + "%")

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument(
        '--env',
        type=str,
        default='uno',
        choices=[
            'blackjack',
            'leduc-holdem',
            'limit-holdem',
            'doudizhu',
            'mahjong',
            'no-limit-holdem',
            'uno',
            'gin-rummy',
        ],
    )
    parser.add_argument(
        '--models',
        nargs='*',
        default=[
            'experiments/uno_nfsp_result/model.pth',
            'random',
            'random',
        ], # add in our own model here later when we change it
        # compare against regular model, our model, and random
        # but may need to adjust player size (from 2 to 3)
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=257,
    ) # 257 gave highest for 10,000 - 34.56%

    parser.add_argument(
        '--num_games',
        type=int,
        default=10000,
    )
     

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    evaluate(args)

