import re

with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

# Fix header spacing
content = content.replace(
    "print(f\"{Colors.DIM}  {'#':<3} │ {col_time:<14} │ {col_id_tag:<20} │ {col_preview}{Colors.RESET}\")",
    "print(f\"{Colors.DIM}   {'#':<3} │ {col_time:<14} │ {col_id_tag:<20} │ {col_preview}{Colors.RESET}\")"
)
content = content.replace(
    "print(f\"{Colors.DIM} ─────┼────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────{Colors.RESET}\")",
    "print(f\"{Colors.DIM} ──────┼────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────{Colors.RESET}\")"
)
content = content.replace(
    "print(f\"{Colors.DIM} ─────┴────────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────────{Colors.RESET}\\n\")",
    "print(f\"{Colors.DIM} ──────┴────────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────────{Colors.RESET}\\n\")"
)

# Fix selected row highlight
old_block = """        if is_selected:
            # Invert the entire line so gaps don't appear
            idx_pad = f"{idx:<3}"
            rel_pad = f"{s['relative']:<14}"
            # Re-apply bold/color to prompt if it has search highlight, 
            # but since inverted overrides foreground, we just print the raw line inverted
            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
                
            print(f"\\033[7m  {idx_pad} │ {rel_pad} │ {id_tag_str} │ {raw_prompt}\\033[0m")
        else:
            idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            cid_str = f"{Colors.GREEN}{id_tag_str}{Colors.RESET}"
            prompt_str = f"{Colors.RESET}{prompt_trunc}"
            print(f"  {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")"""

new_block = """        if is_selected:
            # Modern highlight: Pointer + Bold Vibrant Colors instead of blocky inversion
            idx_str = f"{Colors.BOLD}{Colors.CYAN}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.BOLD}{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            cid_str = f"{Colors.BOLD}{Colors.CYAN}{id_tag_str}{Colors.RESET}"
            
            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}{raw_prompt}{Colors.RESET}"
            
            print(f" {Colors.BOLD}{Colors.CYAN}➜{Colors.RESET} {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")
        else:
            idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            cid_str = f"{Colors.GREEN}{id_tag_str}{Colors.RESET}"
            prompt_str = f"{Colors.RESET}{prompt_trunc}"
            print(f"   {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")"""

content = content.replace(old_block, new_block)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
