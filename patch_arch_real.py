import re

with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

pattern = re.compile(r'    arch_logo = \[\n.*?\]\n    pads_arch = \[.*?\]\n', re.DOTALL)

new_arch_logo = """    arch_logo = [
        '\\x1b[38;2;23;147;209m            ▄██▄            \\x1b[m',
        '\\x1b[38;2;23;147;209m          ▄██████▄          \\x1b[m',
        '\\x1b[38;2;23;147;209m        ▄██████████▄        \\x1b[m',
        '\\x1b[38;2;23;147;209m      ▄███▀▀    ▀▀███▄      \\x1b[m',
        '\\x1b[38;2;23;147;209m    ▄███▀    ▄▄    ▀███▄    \\x1b[m',
        '\\x1b[38;2;23;147;209m  ▄███▀    ▄█▀▀█▄    ▀▀▀█▄  \\x1b[m',
        '\\x1b[38;2;23;147;209m▄███▀                  ▀███▄\\x1b[m'
    ]
    pads_arch = ["  ", "  ", "  ", "  ", "  ", "  ", "  "]
"""

content = pattern.sub(new_arch_logo, content, count=1)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
