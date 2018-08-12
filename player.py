from copy import copy

from card import PlayerCards

class Player(object):
    """docstring for Player"""
    def __init__(self, id):
        super(Player, self).__init__()
        self.id = id
        
        self._score_cards_obj = PlayerCards([])
        self._hand_cards_obj = None
        self._opposite_cards_obj = None

    def obtain_handcards(self, raw_cards):
        self._hand_cards_obj = PlayerCards(raw_cards)

    def pick_out_cards(self, number_of_picked=3):
        drop_cards = []

        # pick based on the length of shape
        for shape, length in self._hand_cards_obj.current_length_list:
            if 0 < length <= number_of_picked:
                drop_cards.extend(self._hand_cards_obj.current_cards_dict[shape])
            if len(drop_cards) >= number_of_picked:
                break
        if drop_cards:
            self._hand_cards_obj.drop_cards(drop_cards)

        # pick based on the BIG_SCORE_CARDS
        for card in [('S', 12), ('H', 14), ('H', 13), ('H', 12), ('H', 11)]:
            if card in self._hand_cards_obj.current_cards_list:
                drop_cards.append(card)
                self._hand_cards_obj.drop_one_card(card)
            if len(drop_cards) >= number_of_picked:
                break

        # pick based on the BIGGEST_NUMBER cards
        if len(drop_cards) < number_of_picked:
            lacked_cards = self._hand_cards_obj.current_cards_list[(len(drop_cards) - number_of_picked):]
            drop_cards.extend(lacked_cards)
            self._hand_cards_obj.drop_cards(lacked_cards)

        print 'player %d drop cards' % self.id, drop_cards
        return drop_cards

    def get_transfered_cards(self, cards):
        self._hand_cards_obj.add_cares(cards)      

        print 'player %d get cards' % self.id, cards

    def is_first_master(self):
        return self._hand_cards_obj.is_first_master()

    def show_cards(self):
        cards_can_show = self._hand_cards_obj.cards_can_show()

        if self._hand_cards_obj.current_length_list[0][1] == 0:
            return cards_can_show
        else:
            return []

    def get_shown_cards(self, shown_cards):
        for cards_list in show_cards:
            self._hand_cards_obj.add_shown_cards(cards_list)


    def play(self, round, public_cards):
        if self._opposite_cards_obj is None:
            self._opposite_cards_obj = PlayerCards(self._hand_cards_obj.get_opposite_cards())

        






class Player(object):
    """docstring for Player"""
    def __init__(self, id):
        super(Player, self).__init__()
        self.id = id

        self.owned_scores = 0


    def get_cards(self, raw_cards):
        self.raw_cards = raw_cards
        self.raw_formated_cards = self.format_cards(self.raw_cards)
        self.current_cards = copy(self.raw_formated_cards)
        self.smashed = False
        self.round_cards = []
        self.history_hands = []

    def drop_three_cards(self):
        drop_cards = []

        cards_length = self.get_cards_length()
        for shape,length in cards_length:
            if 4 >= length > 0:
                drop_cards = self.current_cards[shape][-3:]
                self.current_cards[shape] = self.current_cards[shape][:-3]
                break
        if len(drop_cards) < 3:
            for card in [('b', 12), ('a', 11), ('a', 12), ('a', 13), ('a', 14)]:
                if len(drop_cards) >= 3:
                    break

                cards_list = self.get_cards_list()
                if card in cards_list:
                    drop_cards.append(card)
                    self.current_cards[card[0]].remove(card)

        while len(drop_cards) < 3:
            cards_list = self.get_cards_list()
            card = cards_list[-1]
            drop_cards.append(card)
            self.current_cards[card[0]].remove(card)

        print 'player %d drop cards' % self.id, drop_cards
        return drop_cards

    def get_three_cards(self, three_cards):
        print 'player %d get cards' % self.id, three_cards





    def format_cards(self, cards_list):
        cards_dict = {
            'a': [],
            'b': [],
            'c': [],
            'd': []
        }
        # aggregate
        for shape, num in cards_list:
            cards_dict[shape].append((shape, int(num)))

        # rank        
        for shape in cards_dict:
            cards_dict[shape].sort(key=lambda item:item[1])

        return cards_dict
        
    def is_first_master(self):
        return True if ('d', 2) in self.raw_formated_cards['d'] else False

    def get_cards_length(self):
        cards_length = [(shape, len(self.current_cards[shape])) for shape in self.current_cards]
        cards_length.sort(key=lambda item: item[1])
        return cards_length

    def get_cards_list(self):
        cards_list = []
        for shape in self.current_cards:
            cards_list.extend(self.current_cards[shape])
        cards_list.sort(key=lambda item: item[1])
        return cards_list

    def play(self, public_cards):
        cards_length = self.get_cards_length()
        if len(public_cards) == 0: # master
            if ('d', 2) in self.current_cards['d']:
                card = ('d', 2)
                self.current_cards['d'].remove(card)
            else:
                for shape, length in cards_length:
                    if self.smashed is False and shape == 'a': # can not play red cards first
                        continue
                    if length == 0:
                        continue
                    break
                # get lest cards    
                card = self.current_cards[shape].pop(0)
        else:
            shape = public_cards[0][1][0]
            if self.current_cards[shape]:
                card = self.current_cards[shape].pop(0)
            else: # 
                if ('b', 12) in self.current_cards['b']:
                    card = ('b', 12)
                    self.current_cards['b'].remove(card)
                elif self.current_cards['a']and self.current_cards['a'][-1][1] > 5:
                    card = self.current_cards['a'].pop(-1)
                elif self.current_cards['b']and self.current_cards['b'][-1][1] > 12:
                    card = self.current_cards['b'].pop(-1)
                else:
                    cards_list = self.get_cards_list()
                    card = cards_list[-1]
                    self.current_cards[card[0]].remove(card)

        print "play %d play: " % self.id, card, 'current cards length', len(self.get_cards_list())

        public_cards.append((self.id, card))

    def store(self, round_master, public_cards):
        if self.id == round_master:
            self.round_cards.extend(public_cards)

        self.history_hands.append(public_cards)


    def get_round_score(self):
        score = 0
        for id, card in self.round_cards:
            if card[0] == 'a': # 1 score
                score += 1
            elif card == ('b', 12): # 13 score
                score += 13

        return score

    def store_round_score(self, score=None):
        self.owned_scores += score if score is not None else self.get_round_score()













