import re
from typing import List, Dict
from agy_sessions.ui.colors import Colors
from agy_sessions.i18n.manager import _t

def print_beautiful_table(sessions: List[Dict], total_count: int, start_idx: int, page: int, total_pages: int, search_query: str = ""):
    """Render a beautiful, dependency-free terminal UI table."""
    print("\033[H\033[J", end="")
    
    title = _t('title')
    if search_query:
        title += _t('search_suffix', query=search_query)
        
    stats_line = _t('total_chats_page', count=total_count, page=page, total=total_pages) if total_pages > 0 else _t('total_chats', count=total_count)

    print(f"\n{Colors.BOLD}{Colors.CYAN}╭{'─'*117}╮")
    print(f"│ {title.center(115)} │")
    print(f"│ {stats_line.center(115)} │")
    print(f"╰{'─'*117}╯{Colors.RESET}")

    col_time = _t('col_time')
    col_id_tag = _t('col_id_tag')
    col_preview = _t('col_preview')

    print(f"{Colors.DIM}  {'#':<3} │ {col_time:<14} │ {col_id_tag:<20} │ {col_preview}{Colors.RESET}")
    print(f"{Colors.DIM} ─────┼────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────{Colors.RESET}")

    for i, s in enumerate(sessions):
        idx = start_idx + i + 1
        prompt = s['prompt']
        max_len = 71
        prompt_trunc = prompt[:max_len] + '...' if len(prompt) > max_len else prompt.ljust(max_len)
        short_id = s['id'][:8]
        
        pin_indicator = "📌 " if s['pinned'] else ""
        if s['tag']:
            clean_tag = ' '.join(s['tag'].split())
            max_tag_len = 20 - len(pin_indicator) - len(f" ({short_id})")
            if len(clean_tag) > max_tag_len:
                tag_trunc = clean_tag[:max_tag_len-2] + '..'
            else:
                tag_trunc = clean_tag
            id_tag_str = f"{pin_indicator}{tag_trunc} ({short_id})"
        else:
            id_tag_str = f"{pin_indicator}{short_id}"
            
        id_tag_str = id_tag_str.ljust(20)
        
        idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
        time_str = f"{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
        cid_str = f"{Colors.GREEN}{id_tag_str}{Colors.RESET}"
        
        # Highlight search query in prompt if exists
        if search_query:
            insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
            prompt_trunc = insensitive_query.sub(rf"{Colors.BOLD}{Colors.MAGENTA}\g<0>{Colors.RESET}", prompt_trunc)

        prompt_str = f"{Colors.RESET}{prompt_trunc}"
        print(f"  {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")

    print(f"{Colors.DIM} ─────┴────────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────────{Colors.RESET}\n")
