import re

# Fix table.py
with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

old_block = """        if is_selected:
            # Inverted colors for selected row
            idx_str = f"\\033[7m  {idx:<3}\\033[0m"
            time_str = f"\\033[7m{s['relative']:<14}\\033[0m"
            cid_str = f"\\033[7m{id_tag_str}\\033[0m"
            prompt_str = f"\\033[7m{prompt_trunc}\\033[0m"
            print(f" {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")
        else:
            idx_str = f"{Colors.BOLD}{Colors.YELLOW}{idx:<3}{Colors.RESET}"
            time_str = f"{Colors.CYAN}{s['relative']:<14}{Colors.RESET}"
            cid_str = f"{Colors.GREEN}{id_tag_str}{Colors.RESET}"
            prompt_str = f"{Colors.RESET}{prompt_trunc}"
            print(f"  {idx_str} │ {time_str} │ {cid_str} │ {prompt_str}")"""

new_block = """        if is_selected:
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

content = content.replace(old_block, new_block)
with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)

# Fix cli.py
with open("agy_sessions/cli.py", "r") as f:
    cli_content = f.read()

cli_content = cli_content.replace(
    "print(f\" ❯ {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET} {input_buffer}\", end=\"\")",
    "print(f\" {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET} {input_buffer}\", end=\"\")"
)
with open("agy_sessions/cli.py", "w") as f:
    f.write(cli_content)

