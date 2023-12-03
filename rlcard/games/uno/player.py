from rlcard.games.uno.payoffs import Payoffs

class UnoPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.stack = []

        # new vars:
        self.reward = 0
        self.previous_legal_actions_ratio = None
        self.valid_card_count = 0
        self.legal_actions = []

    def get_player_id(self):
        ''' Return the id of the player
        '''

        return self.player_id
    

    # new funcs:
    def get_player_reward(self):
        '''Return the reward of the player
        '''
        return self.reward
    

    def get_count_of_color(self, target_color):
        count = 0
        for card in self.hand:
            # print("Card:", card.get_str())
            if 'wild' not in card.trait and card.color == target_color:
                count += 1
        return count
    
    def get_max_color_count(self):
        reds = self.get_count_of_color('r')
        greens = self.get_count_of_color('g')
        blues = self.get_count_of_color('b')
        yellows = self.get_count_of_color('y')
        return max(reds, greens, blues, yellows)
    
    def get_count_of_wilds(self):
        count = 0
        for card in self.hand:
            # print("Card:", card.get_str())
            if 'wild' in card.trait:
                count += 1
        return count
    

    def judge_decision(self, chosen_color, chosen_trait):
        '''Rewards or punishes the agent based on whether it believes its chosen card was a smart play or a mistake
        Takes in the color and trait of the chosen card
        color = 'b', 'r', 'y', 'g'
        trait = number or effect (e.g. '0', 'skip', 'draw_2', 'wild', 'wild_draw_4')
        '''
        # subtracting 1 extra because self.valid_card_count is from before the wild got popped
        other_options = (self.valid_card_count - 1) - self.get_count_of_wilds()
        current_color_options = self.get_count_of_color(chosen_color)
        if 'wild' in chosen_trait:
            if other_options > 0:
                self.adjust_reward(Payoffs.USED_WILD_CARD_WHEN_HAD_OTHER_VALID_OPTIONS.value)
                # if self.player_id == 0:
                #     print("Used wild card when had other options | Current Reward:", self.reward)
            max_potential_color_options = self.get_max_color_count() 
            could_of_had_options = max_potential_color_options - current_color_options
            self.adjust_reward(Payoffs.LOST_VALID_OPTIONS_PER_CARD.value * could_of_had_options)
            # if self.player_id == 0:
            #     print("Used wild card and lost", could_of_had_options, "valid options | Current Reward:", self.reward)
            if (could_of_had_options == max_potential_color_options):
                self.adjust_reward(Payoffs.OPTIMIZED_WILD_CARD.value)
                # if self.player_id == 0:
                #     print("Used optimized wild card | Current Reward:", self.reward)
        elif chosen_trait not in "0123456789":
            # you want to save draw_2s but use skips and reverses ASAP
            if chosen_trait == 'draw_2':
                self.adjust_reward(Payoffs.USED_DRAW_2_CARD.value)
                # if self.player_id == 0:
                #     print("Used draw 2 card | Current Reward:", self.reward)
            elif chosen_trait == 'skip' or chosen_trait == 'reverse':
                self.adjust_reward(Payoffs.USED_SKIP_OR_REVERSE_CARD.value)
                # if self.player_id == 0:
                #     print("Used skip or reverse | Current Reward:", self.reward)
        else:
            # TODO: check in legal actions and see if you could have picked another normal card that gave you more options
            self.adjust_reward(Payoffs.USED_NORMAL_CARD.value)
            # if self.player_id == 0:
            #     print("Used normal card | Current Reward:", self.reward)


    def adjust_reward(self, amount):
        self.reward += amount
