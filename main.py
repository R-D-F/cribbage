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


def print_hand(hand):
    for c in hand:
        print_card(c.rank, c.suit)


def print_hand_simplified(hand):
    to_print = ""
    for c in hand:
        to_print += f"{c.suit}/{c.rank}  "

    print(to_print)


def equals_15(cards: list[Card]):
    combo_value = 0
    for card in cards:
        combo_value += card.value
    if combo_value == 15:
        return True
    else:
        return False


def score_hand(hand: list[Card], discard: list[Card]):
    max_score = 0
    best_hand = []
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    deck_without_hand = [card for card in deck if card not in hand]
    hand = list(hand)
    average = 0

    for card in deck_without_hand:
        current_hand = []
        current_hand.extend(hand)
        score = 0
        current_hand.append(card)
        # print_hand_simplified(current_hand)

        for two_card_combo in combinations(current_hand, 2):
            if equals_15(two_card_combo):
                score += 2
        for three_card_combo in combinations(current_hand, 3):
            if equals_15(three_card_combo):
                score += 2
        for four_card_combo in combinations(current_hand, 4):
            if equals_15(four_card_combo):
                score += 2
        for five_card_combo in combinations(current_hand, 5):
            if equals_15(five_card_combo):
                score += 2
        if score > max_score:
            max_score = score
            best_hand = current_hand
        average += score
    average = average / len(deck_without_hand)
    return best_hand, max_score, average


def score_discard(hand: list[Card], discard: list[Card]):
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    pass


def find_best_hand(hand: list[Card]) -> list[Card]:

    best_average_hand = 0
    best_possible_hand = []
    for combo in combinations(hand, 4):
        discard = []

        for card in hand:
            if card not in combo:
                discard.append(card)

        (best_hand, hand_score, average) = score_hand(combo, discard)

        discard_score = score_discard(combo, discard)
        # print_hand_simplified(best_hand)
        # print(f"hand_score = {hand_score}")
        # print(f"Average = {average}")
        if average > best_average_hand:
            best_average_hand = average
            best_possible_hand = combo
    return best_possible_hand, best_average_hand


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

print_hand_simplified(hand_a)
best_possible_hand, best_average_hand = find_best_hand(hand_a)
print_hand_simplified(best_possible_hand)
print(best_average_hand)
