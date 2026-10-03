with open("agy_sessions/cli.py", "r") as f:
    content = f.read()

old_print = """            # We don't use input() anymore, just print instructions
            print(f" {Colors.BOLD}{color}Use ⬆/⬇ to navigate, ENTER to {action_text}, 'n' for new session, 'q' to quit.{Colors.RESET}")
            sys.stdout.flush()"""

new_print = """            # We don't use input() anymore, just print instructions
            prompt_actions = [_t('prompt_actions', action=action_text), _t('prompt_new_opt')]
            if total_pages > 1:
                prompt_actions.append(_t('prompt_nav'))
            prompt_str = ", ".join(prompt_actions)
            print(f" ❯ {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET}", end="")
            sys.stdout.flush()"""

content = content.replace(old_print, new_print)

with open("agy_sessions/cli.py", "w") as f:
    f.write(content)
