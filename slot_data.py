def get_symbols_per_line(reel_heights, symbol_list):
    max_reel = len(reel_heights)
    max_row = reel_heights[0]
    lines = [[None for reel in range(max_reel)] for row in range(max_row)]
    for reel in range(max_reel):
        for row in range(max_row):
            lines[row][reel] = symbol_list[max_row * reel + row]
    return lines
