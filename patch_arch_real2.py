import re

with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

match = re.search(r'    arch_logo = \[\n.*?\]\n    pads_arch = \[.*?\]\n', content, flags=re.DOTALL)
old_arch = match.group(0)

new_arch_logo = """    arch_logo = [
        '\\x1b[38;2;23;147;209m            ▄██▄            \\x1b[m',
        '\\x1b[38;2;23;147;209m          ▄██████▄          \\x1b[m',
        '\\x1b[38;2;23;147;209m        ▄██████████▄        \\x1b[m',
        '\\x1b[38;2;23;147;209m      ▄███▀▀    ▀▀███▄      \\x1b[m',
        '\\x1b[38;2;23;147;209m    ▄███▀    ▄▄    ▀███▄    \\x1b[m',
        '\\x1b[38;2;23;147;209m  ▄███▀    ▄█▀▀█▄    ▀▀▀█▄  \\x1b[m',
        '\\x1b[38;2;23;147;209m▄███▀                  ▀███▄\\x1b[m'
    ]
    pads_arch = ["", "", "", "", "", "", ""]
"""

content = content.replace(old_arch, new_arch_logo)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
