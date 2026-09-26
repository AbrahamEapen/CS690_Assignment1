def top_k_frequent(items, k):
    from collections import OrderedDict

    if k == 0:
        return []

    counts = OrderedDict()
    for item in items:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    return [
        item
        for item, _ in sorted(
            counts.items(),
            key=lambda pair: -pair[1],
        )[:k]
    ]
