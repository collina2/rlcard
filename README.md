# RL Techniques for UNO

By Andrew Collins, Rithvij Pochampally, and Kirby Ammari

## Setup

Ensure you are in the RLCARD home directory, and run these commands:

```
pip3 install -e .
pip3 install -e '.[torch]'
```

## Running Examples

```
cd examples
```

### To Run a Training of the DQN Model

This will train the DQN Agent with Custom Rewards

```
python run_rl.py
```

### To Run the Evaluation 

This will run a game between the Old DQN Agent, New DQN Agent, and Random Agent

```
python evaluate.py
```
