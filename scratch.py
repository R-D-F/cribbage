def runs(hand):
    """
    In cribbage, a player has a hand of 5 cards when counting points.

    If a player has a hand with 3 sequential cards in a row, they are awarded 3 points.
    Same goes for a run of 4 and a run of 5, each awarding 4 and 5 points, respectively.

    For example if I have a hand: [1,2,3,6,8] (usually in the form of playing cards),
    I would earn 3 points, for the run of three in the first three elements of the list.
    """
    # sort hand ascending order
    hand = sorted(hand)

    # get longest sequence
    totalpoints = 1
    for i in range(4):
        if hand[i + 1] == hand[i] + 1:
            totalpoints += 1
        elif totalpoints < 3:
            totalpoints = 1

    # score if continuous sequence is greater or equal than 3
    if totalpoints < 3:
        totalpoints = 0

    return totalpoints


hand = [1, 2, 3, 2, 5]

print(runs(hand))
