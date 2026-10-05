with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

import re

old_header_pattern = r'    print\(f"\\n\{Colors\.BOLD\}\{Colors\.CYAN\}╭\{\'─\'\*117\}╮"\).*?print\(f"╰\{\'─\'\*117\}╯\{Colors\.RESET\}"\)'

new_header = """    logo = [
        f"     {Colors.L1}▄▄{Colors.RESET}",
        f"    {Colors.L2}████{Colors.RESET}",
        f"   {Colors.L3}██████{Colors.RESET}",
        f"   {Colors.L4}██{Colors.RESET}  {Colors.L4}██{Colors.RESET}",
        f"  {Colors.L5}██{Colors.RESET}    {Colors.L5}██{Colors.RESET}",
        f"  {Colors.L6}▀▀{Colors.RESET}    {Colors.L6}▀▀{Colors.RESET}"
    ]
    
    lines = [
        "",
        f"{Colors.BOLD}{title}{Colors.RESET}",
        f"{Colors.DIM}{stats_line}{Colors.RESET}",
        "",
        "",
        ""
    ]
    
    print()
    for i in range(6):
        print(f" {logo[i]}    {lines[i]}")
    print()"""

content = re.sub(old_header_pattern, new_header, content, flags=re.DOTALL)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
