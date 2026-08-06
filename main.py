from random import choices


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


suits = ["heart", "diamonds", "spades", "clubs"]
values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

deck = [Card(value, suit) for value in values for suit in suits]

dealt_pool = choices(deck, k=13)
for card in dealt_pool:
    print(card.suit)
    print(card.value)
print("##################")
hand_a = dealt_pool[0:11:2]
hand_b = dealt_pool[1:12:2]
cut = dealt_pool[12]

print(cut.suit)
print(cut.value)
print("##################")
for card in hand_b:
    print(card.suit)
    print(card.value)
