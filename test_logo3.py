class Colors:
    CYAN = '\033[36m'
    MAGENTA = '\033[35m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    # Logo gradient colors
    L1 = '\033[38;2;250;171;19m' # Orange/Yellow
    L2 = '\033[38;2;234;67;53m'  # Red/Pink
    L3 = '\033[38;2;155;38;175m' # Purple
    L4 = '\033[38;2;25;103;210m' # Blue
    L5 = '\033[38;2;66;133;244m' # Light Blue
    L6 = '\033[38;2;36;193;224m' # Cyan
    
def print_header(total_count, page, total_pages):
    print("\033[H\033[J", end="")
    
    logo = [
        f"     {Colors.L1}▄▄{Colors.RESET}",
        f"    {Colors.L2}████{Colors.RESET}",
        f"   {Colors.L3}██████{Colors.RESET}",
        f"   {Colors.L4}██{Colors.RESET}  {Colors.L4}██{Colors.RESET}",
        f"  {Colors.L5}██{Colors.RESET}    {Colors.L5}██{Colors.RESET}",
        f"  {Colors.L6}▀▀{Colors.RESET}    {Colors.L6}▀▀{Colors.RESET}"
    ]
    
    stats_line = f"Jami chatlar: {total_count} | Sahifa {page}/{total_pages}"
    
    lines = [
        f"{Colors.BOLD}AgyHub (Antigravity Sessiya Menejeri){Colors.RESET}",
        f"{Colors.DIM}{stats_line}{Colors.RESET}",
        "",
        "",
        "",
        ""
    ]
    
    print()
    for i in range(6):
        if i < 2:
            print(f" {logo[i]}    {lines[i]}")
        else:
            print(f" {logo[i]}")
    
    print(f"\n{Colors.DIM}{'─'*117}{Colors.RESET}")

print_header(299, 1, 20)
