from typing import List
from agychat.ui.colors import Colors

def print_accounts_table(accounts: List[str], current_email: str, selected_idx: int):
    """Render a beautiful terminal UI table for accounts."""
    print("\033[2J\033[H", end="")
    
    title = "Antigravity Account Switcher"
    stats_line = f"Total Saved Accounts: {len(accounts)}"

    logo = [
        '     \x1b[38;2;219;177;49m▄\x1b[38;2;242;146;46;48;2;246;145;46m▀\x1b[38;2;240;114;54;48;2;243;115;55m▀\x1b[38;2;240;88;59;49m▄\x1b[m',
        '    \x1b[38;2;158;195;69;48;2;134;198;78m▀\x1b[38;2;181;180;62;48;2;117;180;94m▀\x1b[38;2;226;153;61;48;2;204;149;77m▀\x1b[38;2;246;122;52;48;2;239;121;71m▀\x1b[38;2;248;106;53;48;2;225;102;82m▀\x1b[38;2;239;84;66;48;2;225;79;89m▀\x1b[m',
        '   \x1b[38;2;124;194;81;48;2;128;198;84m▀\x1b[38;2;113;194;92;48;2;84;184;129m▀\x1b[38;2;92;169;143;48;2;64;151;222m▀\x1b[38;2;92;145;179;49m▀\x1b[38;2;131;115;176m▀\x1b[38;2;116;111;195;48;2;74;126;228m▀\x1b[38;2;153;93;168;48;2;112;110;206m▀\x1b[38;2;156;91;151;48;2;143;100;180m▀\x1b[m',
        '  \x1b[38;2;109;198;148m▄\x1b[38;2;97;195;125;48;2;98;186;213m▀\x1b[38;2;67;174;171;48;2;71;168;220m▀\x1b[m    \x1b[38;2;74;128;234;48;2;61;137;251m▀\x1b[38;2;108;115;216;48;2;74;129;240m▀\x1b[38;2;101;121;225;49m▄\x1b[m',
        ' \x1b[38;2;103;185;244m▄\x1b[38;2;107;199;163;48;2;100;182;246m▀\x1b[38;2;100;182;246;49m▀\x1b[m      \x1b[38;2;56;134;251m▀\x1b[38;2;72;129;244;48;2;56;131;249m▀\x1b[38;2;61;133;252;49m▄\x1b[m'
    ]
    pads_logo = ["     ", "    ", "   ", "  ", " "]

    text_lines = [
        "",
        f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.RESET}",
        f"{Colors.DIM}{stats_line}{Colors.RESET}",
        "",
        ""
    ]
    
    print()
    for i in range(5):
        print(f" {logo[i]}{pads_logo[i]}    {text_lines[i]}")
    print()

    print(f"{Colors.DIM}   {'#':<3} │ {'STATUS':<14} │ ACCOUNT EMAIL{Colors.RESET}")
    print(f"{Colors.DIM} ──────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────{Colors.RESET}")

    if not accounts:
        print(f"       │                │ {Colors.YELLOW}No accounts saved. Press [s] to save current login.{Colors.RESET}")
    else:
        for i, email in enumerate(accounts):
            idx = i + 1
            is_active = (email == current_email)
            status_text = "ACTIVE" if is_active else "Standby"
            
            is_selected = (i == selected_idx)
            
            pad_len = 94 - len(email)
            padded_email = email + (" " * pad_len)
            
            if is_selected:
                raw_line = f"{idx:<3} │ {status_text:<14} │ {padded_email}"
                
                bg = "\033[48;5;39m"  # Blue background
                fg_black = "\033[38;5;232m" # Black text
                fg_blue = "\033[38;5;39m"  # Blue foreground
                reset = "\033[0m"
                
                pill_left = f"{fg_blue}{bg}{fg_black}"
                pill_right = f"{reset}{fg_blue}{reset}"
                
                print(f"  {pill_left}{raw_line}{pill_right}")
            else:
                idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
                if is_active:
                    status_str = f"{Colors.GREEN}{Colors.BOLD}{status_text:<14}{Colors.RESET}"
                    email_str = f"{Colors.GREEN}{Colors.BOLD}{padded_email}{Colors.RESET}"
                else:
                    status_str = f"{Colors.DIM}{status_text:<14}{Colors.RESET}"
                    email_str = f"{Colors.RESET}{padded_email}{Colors.RESET}"
                    
                print(f"   {idx_str} │ {status_str} │ {email_str}")

    print(f"{Colors.DIM} ──────┴────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────{Colors.RESET}\n")
