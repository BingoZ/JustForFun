from copy import copy
import numpy as np

class BaseCard(object):
    """docstring for Card"""

    CARD_NUMBER = xrange(2, 15)
    CARD_SHAPE =  ['H', 'S', 'C', 'D'] # H(红心), S(黑桃), C(草花), D(方块)

    PIG = ('S', 12)
    STAR = ('H', 2) # - H14
    FIRST_MASTER = ('C', 2)

    def __init__(self):
        super(Card, self).__init__()

        self.num_func = lambda x: x[1]

        

class PlayerCards(BaseCard):
    """docstring for PlayerCard"""
    def __init__(self, cards_list):
        super(PlayerCard, self).__init__()
        self.raw_cards_list = cards_list

        self.current_cards_list = copy(self.raw_cards_list)

        self.flush()

    def flush(self):
        self.current_cards_list.sort(key=self.num_func)

        # get current dict
        self.current_cards_dict = {
            'H': [],
            'S': [],
            'C': [],
            'D': []
        }
        for shape, num in self.current_cards_list:
            self.current_cards_dict[shape].append((shape, num))
        for shape in self.current_cards_dict:
            self.current_cards_dict[shape].sort(self.num_func)

        # get length dict
        self.current_length_list = [(shape, len(self.current_length_dict[shape])) for shape in self.current_cards_dict]
        self.current_length_list.sort(self.num_func)

    def drop_one_card(self, card):
        self.current_cards_list.remove(card)
        self.flush()

    def add_one_card(self, card):
        self.current_cards_list.append(card)
        self.flush()


class MasterCards(BaseCard):
    """docstring for MasterCards"""
    def __init__(self):
        super(MasterCards, self).__init__()

        self.cards_db = []
        for num in self.CARD_NUMBER:
            for shape in self.CARD_SHAPE:
                self.cards_db.append((shape, num))

        self.cards_db = np.array(self.cards_db)

    def deal(self, num_of_player=4):
        np.random.shuffle(self.cards_db)
        self.dealed_cards = np.split(self.cards_db, num_of_player)

    def output_cards(self, round):
        """
            round: 1-4
        """

        return self.dealed_cards[round:] + self.dealed_cards[:round]