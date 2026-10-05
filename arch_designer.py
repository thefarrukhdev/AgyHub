C = "\x1b[38;2;23;147;209m"
R = "\x1b[m"

grid = [
    "             11             ", # 0
    "            1111            ", # 1
    "           111111           ", # 2
    "          11111111          ", # 3
    "         1111111111         ", # 4
    "        111111111111        ", # 5
    "       11111    11111       ", # 6
    "      1111        1111      ", # 7
    "     1111          1111     ", # 8
    "    1111     11     1111    ", # 9
    "   1111     1111     1111   ", # 10
    "  1111     11  11       11  ", # 11
    " 1111                  1111 ", # 12
    "1111                    1111"  # 13
]

lines = []
for y in range(0, 14, 2):
    line_str = f"{C}"
    for x in range(28):
        upper = grid[y][x] == '1'
        lower = grid[y+1][x] == '1'
        if upper and lower: line_str += "█"
        elif upper and not lower: line_str += "▀"
        elif not upper and lower: line_str += "▄"
        else: line_str += " "
    line_str += f"{R}"
    lines.append(line_str)

for l in lines:
    print(l)
