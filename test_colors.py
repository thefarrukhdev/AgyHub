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
    # True Cyan
    TRUE_CYAN = '\033[38;5;51m'
    TRUE_GREEN = '\033[38;5;46m'
    TRUE_BLUE = '\033[38;5;39m'

print(f"{Colors.TRUE_CYAN}This is true cyan{Colors.RESET}")
