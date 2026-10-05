class Colors:
    L1 = '\033[38;2;250;171;19m' # Orange/Yellow
    L2 = '\033[38;2;234;67;53m'  # Red/Pink
    L3 = '\033[38;2;155;38;175m' # Purple
    L4 = '\033[38;2;25;103;210m' # Blue
    L5 = '\033[38;2;66;133;244m' # Light Blue
    L6 = '\033[38;2;36;193;224m' # Cyan
    R = '\033[0m'
    
logo = [
    f"     {Colors.L1}▄▄{Colors.R}",
    f"    {Colors.L2}████{Colors.R}",
    f"   {Colors.L3}██████{Colors.R}",
    f"   {Colors.L4}██{Colors.R}  {Colors.L4}██{Colors.R}",
    f"  {Colors.L5}██{Colors.R}    {Colors.L5}██{Colors.R}",
    f"  {Colors.L6}▀▀{Colors.R}    {Colors.L6}▀▀{Colors.R}"
]

for l in logo:
    print(l)
