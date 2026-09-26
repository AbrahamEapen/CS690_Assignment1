def window_sums(values, width):
    if width <= 0:
        raise ValueError("width must be positive")
    if width > len(values):
        return []

    total = sum(values[:width])
    result = [total]
    for i in range(width, len(values)):
        total += values[i] - values[i - width]
        result.append(total)
    return result
