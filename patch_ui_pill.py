with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

old_block = """        if is_selected:
            # Modern highlight: Pointer + Bold Vibrant Colors instead of blocky inversion
            idx_str = f"{Colors.BOLD}{Colors.CYAN}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.BOLD}{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            cid_str = f"{Colors.BOLD}{Colors.CYAN}{id_tag_str}{Colors.RESET}"
            
            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
                
            if search_query:
                # Keep search highlight (magenta) but make the rest cyan
                import re
                insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
                raw_prompt = insensitive_query.sub(rf"{Colors.BOLD}{Colors.MAGENTA}\\g<0>{Colors.RESET}{Colors.BOLD}{Colors.CYAN}", raw_prompt)
                
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}{raw_prompt}{Colors.RESET}"
            
            print(f" {Colors.BOLD}{Colors.CYAN}▶{Colors.RESET} {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")
        else:"""

new_block = """        if is_selected:
            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
                
            # Create the raw 117-char line without any ANSI colors
            raw_line = f"{idx:<3} │ {s['relative']:<14} │ {id_tag_str} │ {raw_prompt}"
            
            bg = "\\033[48;5;39m"  # Blue background
            fg_black = "\\033[38;5;232m" # Black text
            fg_blue = "\\033[38;5;39m"  # Blue foreground
            reset = "\\033[0m"
            
            if search_query:
                import re
                insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
                # Pink text for search highlight, back to black
                raw_line = insensitive_query.sub(rf"\\033[38;5;199m\\033[1m\\g<0>\\033[22m{fg_black}", raw_line)

            pill_left = f"{fg_blue}{bg}{fg_black}"
            pill_right = f"{reset}{fg_blue}{reset}"
            
            print(f"  {pill_left}{raw_line}{pill_right}")
        else:"""

content = content.replace(old_block, new_block)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
