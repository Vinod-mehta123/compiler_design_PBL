def optimize(inter_code):
    # Dummy constant folding optimization
    optimized = []
    for line in inter_code:
        if len(line) == 5 and line[2].isdigit() and line[4].isdigit():
            result = eval(f"{line[2]} {line[3]} {line[4]}")
            optimized.append((line[0], '=', str(result)))
        else:
            optimized.append(line)
    return optimized
