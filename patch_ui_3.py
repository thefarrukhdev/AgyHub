with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

old_block = """            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}{raw_prompt}{Colors.RESET}\""""

new_block = """            raw_prompt = s['prompt']
            if len(raw_prompt) > max_len:
                raw_prompt = raw_prompt[:max_len] + '...'
            else:
                raw_prompt = raw_prompt.ljust(max_len)
                
            if search_query:
                # Keep search highlight (magenta) but make the rest cyan
                import re
                insensitive_query = re.compile(re.escape(search_query), re.IGNORECASE)
                raw_prompt = insensitive_query.sub(rf"{Colors.BOLD}{Colors.MAGENTA}\g<0>{Colors.RESET}{Colors.BOLD}{Colors.CYAN}", raw_prompt)
                
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}{raw_prompt}{Colors.RESET}\""""

content = content.replace(old_block, new_block)

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
