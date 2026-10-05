with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

import re
old_logo = re.search(r'    logo = \[\n.*?\]', content, flags=re.DOTALL).group(0)

new_logo = """    logo = [
        '     \\x1b[38;2;219;177;49m▄\\x1b[38;2;242;146;46;48;2;246;145;46m▀\\x1b[38;2;240;114;54;48;2;243;115;55m▀\\x1b[38;2;240;88;59;49m▄\\x1b[m',
        '    \\x1b[38;2;158;195;69;48;2;134;198;78m▀\\x1b[38;2;181;180;62;48;2;117;180;94m▀\\x1b[38;2;226;153;61;48;2;204;149;77m▀\\x1b[38;2;246;122;52;48;2;239;121;71m▀\\x1b[38;2;248;106;53;48;2;225;102;82m▀\\x1b[38;2;239;84;66;48;2;225;79;89m▀\\x1b[m',
        '   \\x1b[38;2;124;194;81;48;2;128;198;84m▀\\x1b[38;2;113;194;92;48;2;84;184;129m▀\\x1b[38;2;92;169;143;48;2;64;151;222m▀\\x1b[38;2;92;145;179;49m▀\\x1b[38;2;131;115;176m▀\\x1b[38;2;116;111;195;48;2;74;126;228m▀\\x1b[38;2;153;93;168;48;2;112;110;206m▀\\x1b[38;2;156;91;151;48;2;143;100;180m▀\\x1b[m',
        '  \\x1b[38;2;109;198;148m▄\\x1b[38;2;97;195;125;48;2;98;186;213m▀\\x1b[38;2;67;174;171;48;2;71;168;220m▀\\x1b[m    \\x1b[38;2;74;128;234;48;2;61;137;251m▀\\x1b[38;2;108;115;216;48;2;74;129;240m▀\\x1b[38;2;101;121;225;49m▄\\x1b[m',
        ' \\x1b[38;2;103;185;244m▄\\x1b[38;2;107;199;163;48;2;100;182;246m▀\\x1b[38;2;100;182;246;49m▀\\x1b[m      \\x1b[38;2;56;134;251m▀\\x1b[38;2;72;129;244;48;2;56;131;249m▀\\x1b[38;2;61;133;252;49m▄\\x1b[m'
    ]"""

# Since new logo has different visible width, we must recalculate padding!
# Line 0: 5 spaces + 4 char = 9. 
# Line 1: 4 spaces + 6 char = 10.
# Line 2: 3 spaces + 8 char = 11.
# Line 3: 2 spaces + 3 char + 4 spaces + 3 char = 12.
# Line 4: 1 space + 3 char + 6 spaces + 3 char = 13.

# Let's target visible width 13 for all.
# Line 0 needs 4 spaces.
# Line 1 needs 3 spaces.
# Line 2 needs 2 spaces.
# Line 3 needs 1 space.
# Line 4 needs 0 spaces.

content = content.replace(old_logo, new_logo)

old_pads = r'pads = \["      ", "     ", "    ", " ", ""\]'
new_pads = 'pads = ["    ", "   ", "  ", " ", ""]'
content = re.sub(old_pads, new_pads, content)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
