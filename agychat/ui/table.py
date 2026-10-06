import re
from typing import List, Dict
from agychat.ui.colors import Colors
from agychat.i18n.manager import _t

def print_beautiful_table(sessions: List[Dict], total_count: int, start_idx: int, page: int, total_pages: int, search_query: str = "", selected_idx: int = -1):
    """Render a beautiful, dependency-free terminal UI table."""
    print("\033[2J\033[H", end="")
    
    title = _t('title')
    if search_query:
        title += _t('search_suffix', query=search_query)
        
    stats_line = _t('total_chats_page', count=total_count, page=page, total=total_pages) if total_pages > 0 else _t('total_chats', count=total_count)

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
        f"{Colors.BOLD}{title}{Colors.RESET}",
        f"{Colors.DIM}{stats_line}{Colors.RESET}",
        "",
        ""
    ]
    
    print()
    for i in range(5):
        print(f" {logo[i]}{pads_logo[i]}    {text_lines[i]}")
    print()

    col_time = _t('col_time')
    col_preview = _t('col_preview')

    print(f"{Colors.DIM}   {'#':<3} │ {col_time:<14} │ {col_preview}{Colors.RESET}")
    print(f"{Colors.DIM} ──────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────{Colors.RESET}")

    for i, s in enumerate(sessions):
        idx = start_idx + i + 1
        prompt = s['prompt'].replace('\n', ' ')
        
        pin_indicator = "📌 " if s.get('pinned') else ""
        if s.get('tag'):
            clean_tag = ' '.join(s['tag'].split())
            tag_raw = f" {pin_indicator}[{clean_tag}]"
            # Use a sleek lavender foreground color instead of an ugly background
            tag_colored = f" {pin_indicator}\033[38;5;141m[{clean_tag}]\033[0m"
        else:
            tag_raw = f" {pin_indicator}" if pin_indicator else ""
            tag_colored = f" {pin_indicator}" if pin_indicator else ""

        max_prompt_len = 94 - len(tag_raw)
        if len(prompt) > max_prompt_len:
            prompt_trunc = prompt[:max_prompt_len-3] + '...'
        else:
            prompt_trunc = prompt
            
        combined_raw = f"{prompt_trunc}{tag_raw}"
        pad_len = 94 - len(combined_raw)
        
        is_selected = (i == selected_idx)
        
        if is_selected:
            padded_combined_raw = combined_raw + (" " * pad_len)
            raw_line = f"{idx:<3} │ {s['relative']:<14} │ {padded_combined_raw}"
            
            bg = "\033[48;5;39m"  # Blue background
            fg_black = "\033[38;5;232m" # Black text
            fg_blue = "\033[38;5;39m"  # Blue foreground
            reset = "\033[0m"
            
            if search_query:
                insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
                raw_line = insensitive_query.sub(rf"\033[38;5;199m\033[1m\g<0>\033[22m{fg_black}", raw_line)

            pill_left = f"{fg_blue}{bg}{fg_black}"
            pill_right = f"{reset}{fg_blue}{reset}"
            
            print(f"  {pill_left}{raw_line}{pill_right}")
        else:
            if search_query:
                insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
                prompt_trunc = insensitive_query.sub(rf"{Colors.BOLD}{Colors.MAGENTA}\g<0>{Colors.RESET}", prompt_trunc)

            idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            prompt_str = f"{Colors.RESET}{prompt_trunc}{tag_colored}" + (" " * pad_len)
            print(f"   {idx_str} │ {time_str} │ {prompt_str}")

    print(f"{Colors.DIM} ──────┴────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────{Colors.RESET}\n")
