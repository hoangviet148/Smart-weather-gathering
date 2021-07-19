def forward(c, mark, k):
    if c == n:
        return 0
    upper_bound = n
    for m in mark:
        if m > c and m < upper_bound:
            upper_bound = m
    min_distance = n + 10
    distances = [(abs(cards[c] - cards[p]), p) for p in range(c+1, upper_bound + 1)]
    try:
        min_distance = sorted(distances, key=lambda x: x[0])[k][0]
        p = sorted([x for x in distances if x[0] == min_distance], key=lambda x: x[1])[-1][1]
    except:
        min_distance, p = sorted(distances, key=lambda x: x[0])[0]
    mark.append(p)
    mark = list(set(mark))
    best = 1000000000
    if c < 10:
        for i in range(3):
            best = min(min_distance + forward(c+1, mark.copy(), i), best)
        return best
    else:
        return min_distance + forward(c+1, mark, 0)

cards = {}
n = 16
for c in range(1, n + 1):
    cards[3**c % (n + 1)] = c


for i in range(3):
    print(forward(1, [], i))