from dataclasses import dataclass
from itertools import combinations
from random import sample

from ascii_cards import print_card


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def value(self):
        values = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10,
        }
        return values[self.rank]


# class Card_2:
#     def __init__(self, rank, suit):
#         self.rank = rank
#         self.suit = suit
#         self.values = {
#             "A": 1,
#             "2": 2,
#             "3": 3,
#             "4": 4,
#             "5": 5,
#             "6": 6,
#             "7": 7,
#             "8": 8,
#             "9": 9,
#             "10": 10,
#             "J": 10,
#             "Q": 10,
#             "K": 10,
#         }
#         self.value = self.values[self.rank]


def print_hand(hand):
    for c in hand:
        print_card(c.rank, c.suit)


def score_hand(hand: list[Card], discard: list[Card]):
    max_score = 0
    best_hand = []
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    deck_without_hand = [card for card in deck if card not in hand]
    hand = list(hand)
    print(hand)
    for card in deck_without_hand:
        score = 0
        hand.append(card)
        print
        for two_card_combo in combinations(hand, 2):
            if two_card_combo[0].value + two_card_combo[1].value == 15:
                score += 2
        if score > max_score:
            max_score = score
            best_hand = hand

    return best_hand, max_score


def score_discard(hand: list[Card], discard: list[Card]):
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    pass


def find_best_hand(hand: list[Card]) -> list[Card]:

    for combo in combinations(hand, 4):
        discard = []

        for card in hand:
            if card not in combo:
                discard.append(card)
        # print("#################HAND##############")
        # for card in combo:
        #     print_card(card.value, card.suit)
        # print("#################DISCARD##############")
        # for card in discard:
        #     print_card(card.value, card.suit)
        hand_score = score_hand(combo, discard)
        print(hand_score)
        discard_score = score_discard(combo, discard)


suits = ("♠", "♥", "♦", "♣")
ranks = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
]


deck = [Card(rank, suit) for rank in ranks for suit in suits]

dealt_pool = sample(deck, k=13)
hand_a = dealt_pool[0:11:2]
hand_b = dealt_pool[1:12:2]
cut = dealt_pool[12]


find_best_hand(hand_a)
