from itertools import combinations


def is_sequential(cards):
    return all(cards[i] + 1 == cards[i + 1] for i in range(len(cards) - 1))


def runs(hand):
    score = 0
    for i in range(5, 2, -1):
        for combo in combinations(hand, i):
            combo = sorted(combo)
            if is_sequential(combo):
                score += len(combo)

    return score


# Runs logic works, need to change value for face cards so that it makes sense with how runs needs to be calculated
hand = [1, 2, 3, 2, 5]

print(runs(hand))


def checkRuns(hand, verbose):
    pips = 0
    hand.sort(key=lambda card: card.rank.value)
    # check for runs starting with 5
    for i in range(5, 2, -1):
        runFound = False
        for combination in combinations(hand, i):
            if all(
                [
                    x.rank.value - y.rank.value == 1
                    for x, y in zip(combination[1:], combination[:-1])
                ]
            ):
                if verbose:
                    print("\tRun for " + str(i) + "! " + cardsString(combination))
                pips += i
                runFound = True

        if runFound:
            return pips

    return pips
