with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

import re

old_loop = r'    print\(\)\n    for i in range\(5\):\n        print\(f" \{logo\[i\]\}    \{lines\[i\]\}"\)\n    print\(\)'

new_loop = """    pads = ["      ", "     ", "    ", " ", ""]
    
    print()
    for i in range(5):
        print(f" {logo[i]}{pads[i]}    {lines[i]}")
    print()"""

content = re.sub(old_loop, new_loop, content, flags=re.DOTALL)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
