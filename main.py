from dataclasses import dataclass
from itertools import combinations

import pandas as pd

from ascii_cards import print_card

rank_to_number = {
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
    "J": 11,
    "Q": 12,
    "K": 13,
}


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


def get_hand_simplified(hand):
    to_print = ""
    for c in hand:
        to_print += f"{c.suit}/{c.rank}  "

    return to_print


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


def fifteens(hand):
    score = 0
    for two_card_combo in combinations(hand, 2):
        if equals_15(two_card_combo):
            score += 2
    for three_card_combo in combinations(hand, 3):
        if equals_15(three_card_combo):
            score += 2
    for four_card_combo in combinations(hand, 4):
        if equals_15(four_card_combo):
            score += 2
    for five_card_combo in combinations(hand, 5):
        if equals_15(five_card_combo):
            score += 2
    return score


def pairs(hand):
    score = 0
    for combo in combinations(hand, 2):
        if combo[0].rank == combo[1].rank:
            score += 2
    return score


def is_sequential(cards):
    return all(cards[i] + 1 == cards[i + 1] for i in range(len(cards) - 1))


def runs(hand):
    # In cribbage, only the longest run length scores,
    # but duplicates can create multiple runs of that same length.
    for run_len in range(5, 2, -1):  # 5, 4, 3
        run_count = 0
        for combo in combinations(hand, run_len):
            ranks_sorted = sorted(rank_to_number[card.rank] for card in combo)
            if is_sequential(ranks_sorted):
                run_count += 1
        if run_count > 0:
            return run_count * run_len
    return 0


def hand_flush(hand, starter_card):
    score = 0
    suits = []
    for card in hand:
        suits.append(card.suit)
    set_suits = set(suits)
    if len(set_suits) == 1:
        score += 4
        if starter_card.suit in set_suits:
            score += 1
    return score


def crib_flush(hand):
    score = 0
    suits = []
    for card in hand:
        suits.append(card.suit)
    set_suits = set(suits)
    if len(set_suits) == 1:
        score += 5

    return score


def knobs(hand, starter_card):
    score = 0
    for card in hand:
        if card.rank == "J":
            if card.suit == starter_card.suit:
                score += 1

    return score


def score_hand(hand: list[Card], discard: list[Card]):
    max_score = 0
    best_hand = []
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    deck_without_hand = [card for card in deck if card not in (*hand, *discard)]
    # deck_without_hand = [Card("K", "♠")]
    hand = list(hand)
    average = 0
    crib_average = 0
    crib_counter = 0
    for starter_card in deck_without_hand:
        current_hand = []
        current_hand.extend(hand)
        score = 0

        flush_score = hand_flush(current_hand, starter_card)
        knobs_score = knobs(current_hand, starter_card)
        # print_hand_simplified(current_hand)
        current_hand.append(starter_card)
        fifteens_score = fifteens(current_hand)
        pairs_score = pairs(current_hand)
        runs_score = runs(current_hand)

        for score_type in [flush_score, knobs_score, fifteens_score, pairs_score, runs_score]:
            score += score_type
        if score > max_score:
            max_score = score
            best_hand = current_hand
        average += score

        deck_without_hand_or_starter_card = [
            card for card in deck_without_hand if card != starter_card
        ]
        for two_card_combo in combinations(deck_without_hand_or_starter_card, 2):
            crib = (*two_card_combo, *discard)
            crib_score = 0
            crib_flush_score = crib_flush((*crib, starter_card))
            crib_knobs = knobs(crib, starter_card)
            crib_fifteens = fifteens((*crib, starter_card))
            crib_pairs = pairs((*crib, starter_card))
            crib_runs = runs((*crib, starter_card))
            for crib_score_type in [
                crib_flush_score,
                crib_knobs,
                crib_fifteens,
                crib_pairs,
                crib_runs,
            ]:
                crib_score += crib_score_type

            crib_counter += 1
            crib_average += crib_score
    average = average / len(deck_without_hand)
    crib_average = crib_average / crib_counter

    return best_hand, max_score, average, crib_average


def rank_hands(hand: list[Card], dealer: bool) -> list[Card]:

    best_average_hand = 0
    best_possible_hand = []
    hand_table = {
        "HAND": [],
        "DISCARD": [],
        # "MAX": [],
        # "MIN": [],
        "HAND AVERAGE": [],
        "CRIB AVERAGE": [],
        "AVERAGE": [],
    }

    for combo in combinations(hand, 4):
        discard = []

        for card in hand:
            if card not in combo:
                discard.append(card)

        if discard == [Card(rank="A", suit="♠"), Card(rank="2", suit="♠")]:
            print_hand_simplified(combo)

        (
            best_hand,
            hand_score,
            average,
            crib_average,
        ) = score_hand(combo, discard)
        hand_table["HAND"].append(get_hand_simplified(combo))
        hand_table["DISCARD"].append(get_hand_simplified(discard))
        # hand_table["MAX"].append("N/A")
        # hand_table["MIN"].append("N/A")
        hand_table["HAND AVERAGE"].append(average)
        hand_table["CRIB AVERAGE"].append(crib_average)
        if dealer:
            hand_table["AVERAGE"].append(average + crib_average)
        else:
            hand_table["AVERAGE"].append(average - crib_average)

    df = pd.DataFrame(hand_table)
    df = df.sort_values(by="AVERAGE", ignore_index=True, ascending=False)
    return df


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

# dealt_pool = sample(deck, k=13)
# hand_a = dealt_pool[0:11:2]
# hand_b = dealt_pool[1:12:2]
# cut = dealt_pool[12]
hand_a = [
    Card("A", "♠"),
    Card("2", "♠"),
    Card("3", "♠"),
    Card("4", "♠"),
    Card("5", "♠"),
    Card("J", "♠"),
]
print_hand_simplified(hand_a)
hand_table = rank_hands(hand_a, True)

print("BEST HAND:")
hand_table.at[0, "HAND"]
print(hand_table)
