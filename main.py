import numpy as np

cards_num = xrange(2, 15) # 2 - A
cards_shape = ['a', 'b', 'c', 'd'] # a -> red, b -> black, c -> fangkuai, d -> meihua

cards_db = []
for num in cards_num:
    for shape in cards_shape:
        cards_db.append((shape, num))

cards_db = np.array(cards_db)

# 12b mean 13 score
# *a mean 1 score each
# 2 d mean the first one chupai


def random_cards(num_of_player=4):
    np.random.shuffle(cards_db)
    return np.split(cards_db, num_of_player)



num_of_player = 4

from player import Player
player_dict = {}
for i in range(num_of_player):
    player_dict[str(i)] = Player(i)

def get_player_list(master, num_of_player=4):
    id_list = []
    for i in range(num_of_player):
        id_list.append((master + i) % num_of_player)

    print 'id_list', id_list

    return [player_dict[str(i)] for i in id_list]

# get raw cards
rc = random_cards(num_of_player)
for i, cards_list in enumerate(rc):
    player_dict[str(i)].get_cards(rc[i])
    print "player %d get cards" % i, rc[i]


def check_public_cards(public_cards):
    shape = public_cards[0][0]

    id_num_list = [(item[0], item[1][1]) for item in public_cards]
    id_num_list.sort(key=lambda item: item[1])
    print "sorted id and card num list is", id_num_list
    return id_num_list[-1][0]

round_master = None
number_of_round = len(rc[0])
round_count = 0
while round_count < number_of_round:
    # prepare
    if round_master is None:
        for player in player_dict.values():
            if player.is_first_master():
                round_master = player.id
                break
    print "round %d, round master is player " % (round_count + 1), round_master

    player_list = get_player_list(round_master)

    # play
    public_cards = []
    for player in player_list:
        player.play(public_cards)

    # store result of this round
    old_round_master = round_master
    round_master = check_public_cards(public_cards)
    print "public cards of this round is ", public_cards
    print 'round master of next round is ', round_master

    for player in player_list:
        player.store(round_master, public_cards)

    round_count += 1

print "round over, time to calculate scores"
all_gotten = None
for player in player_list:
    if player.get_round_score() == 26:
        print "player %d gets all scores" % player.id
        all_gotten = player.id
        break

for player in player_list:
    if all_gotten is None:
        player.store_round_score()
    else:
        if player.id == all_gotten:
            player.store_round_score(0)
        else:
            player.store_round_score(26)

for player in player_list:
    print "player id: %d    score: %d" % (player.id, player.owned_scores)






















