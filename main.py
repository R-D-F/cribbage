from dataclasses import dataclass
from itertools import combinations
from random import sample


@dataclass(frozen=True)
class Card:
    value: str
    suit: str


def score_hand(hand: list[Card], discard: list[Card]):
    deck = [Card(value, suit) for value in values for suit in suits]
    deck_without_hand = [card for card in deck if card not in hand]
    return len(deck_without_hand)


def score_discard(hand: list[Card], discard: list[Card]):
    deck = [Card(value, suit) for value in values for suit in suits]
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
values = [
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

deck = [Card(value, suit) for value in values for suit in suits]

dealt_pool = sample(deck, k=13)
hand_a = dealt_pool[0:11:2]
hand_b = dealt_pool[1:12:2]
cut = dealt_pool[12]


find_best_hand(hand_a)
