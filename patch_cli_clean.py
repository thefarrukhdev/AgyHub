with open("agy_sessions/cli.py", "r") as f:
    content = f.read()

old_block = """        try:
            prompt_actions = [_t('prompt_actions', action=action_text), _t('prompt_new_opt')]
            if total_pages > 1:
                prompt_actions.append(_t('prompt_nav'))
            prompt_str = ", ".join(prompt_actions)
            
            print(f" {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET} {input_buffer}", end="")
            sys.stdout.flush()"""

new_block = """        try:
            # Minimalist prompt
            print(f" {Colors.BOLD}{color}❯ {Colors.RESET}{input_buffer}", end="")
            sys.stdout.flush()"""

content = content.replace(old_block, new_block)

with open("agy_sessions/cli.py", "w") as f:
    f.write(content)
