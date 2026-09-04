x = [
    0,
    1,
    4,
    6,
    3,
    5,
]


def bub_sort(x: list):
    finished = False
    while not finished:
        finished = True
        for e in range(len(x) - 1):
            if x[e] > x[e + 1]:
                x[e], x[e + 1] = x[e + 1], x[e]
                finished = False

    return x


def bubble_sort(values: list[int]) -> list[int]:
    n = len(values)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                swapped = True
        if not swapped:
            break
    return values


def bad_sort(n):
    for i in range(len(n)):
        for j in range(len(n)):
            if n[i] < n[j]:
                n[i], n[j] = n[j], n[i]

    return n


print(bad_sort(x))
