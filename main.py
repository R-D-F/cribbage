from dataclasses import dataclass
from itertools import combinations

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
        if combo[0].value == combo[1].value:
            score += 2
    return score


def is_sequential(cards):
    return all(cards[i] + 1 == cards[i + 1] for i in range(len(cards) - 1))


def runs(hand):
    score = 0
    for i in range(5, 2, -1):
        for combo in combinations(hand, i):
            combo = [rank_to_number[card.rank] for card in combo]
            combo = sorted(combo)
            if is_sequential(combo):
                score += len(combo)

    return score


def hand_flush(hand, starter_card):
    score = 0
    suits = []
    for card in hand:
        suits.append(card.suit)
    set_suits = set(suits)
    if len(set_suits) == 1:
        score += 4
        if starter_card in set_suits:
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
    hand = list(hand)
    average = 0
    crib_average = 0
    crib_counter = 0
    for starter_card in deck_without_hand:
        current_hand = []
        current_hand.extend(hand)
        score = 0

        score += hand_flush(current_hand, starter_card)
        score += knobs(current_hand, starter_card)
        # print_hand_simplified(current_hand)
        current_hand.append(starter_card)
        score += fifteens(current_hand)
        score += pairs(current_hand)
        score += runs(current_hand)

        if score > max_score:
            max_score = score
            best_hand = current_hand
        average += score
    average = average / len(deck_without_hand)

    deck_without_hand_or_starter_card = [card for card in deck if card != starter_card]
    for two_card_combo in combinations(deck_without_hand_or_starter_card, 2):
        crib = (*two_card_combo, *discard)
        crib_score = 0
        crib_score += crib_flush((*crib, starter_card))
        crib_score += knobs(crib, starter_card)
        crib_score += fifteens((*crib, starter_card))
        crib_score += pairs((*crib, starter_card))
        crib_score += runs((*crib, starter_card))
        crib_counter += 1
        crib_average += crib_score
    crib_average = crib_average / crib_counter

    return best_hand, max_score, average, crib_average


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

        (best_hand, hand_score, average, crib_average) = score_hand(combo, discard)

        discard_score = score_discard(combo, discard)
        # print_hand_simplified(best_hand)
        # print(f"hand_score = {hand_score}")
        # print(f"Average = {average}")
        if average + crib_average > best_average_hand:
            best_average_hand = average
            best_possible_hand = combo
    return best_possible_hand, best_average_hand, crib_average


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
best_possible_hand, best_average_hand, crib_average = find_best_hand(hand_a)
print_hand_simplified(best_possible_hand)
print(best_average_hand)
print(crib_average)
