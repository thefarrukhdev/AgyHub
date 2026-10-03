import re

with open("agy_sessions/cli.py", "r") as f:
    content = f.read()

if "from agy_sessions.core.input import read_key" not in content:
    content = content.replace(
        "from agy_sessions.core.db import invalidate_session, update_session_meta",
        "from agy_sessions.core.db import invalidate_session, update_session_meta\nfrom agy_sessions.core.input import read_key"
    )

new_loop = """
    selected_idx = 0
    input_buffer = ""

    while True:
        total_pages = (total_count + limit - 1) // limit
        page = max(1, min(page, total_pages)) if total_pages > 0 else 1
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        displayed_sessions = sessions[start_idx:end_idx]
        
        if selected_idx >= len(displayed_sessions):
            selected_idx = max(0, len(displayed_sessions) - 1)
        if selected_idx < 0:
            selected_idx = 0

        print_beautiful_table(displayed_sessions, total_count=total_count, start_idx=start_idx, page=page, total_pages=total_pages, search_query=args.search, selected_idx=selected_idx)

        try:
            prompt_actions = [_t('prompt_actions', action=action_text), _t('prompt_new_opt')]
            if total_pages > 1:
                prompt_actions.append(_t('prompt_nav'))
            prompt_str = ", ".join(prompt_actions)
            
            print(f" ❯ {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET} {input_buffer}", end="")
            sys.stdout.flush()
            
            key = read_key()
            
            if key in ('q', 'Q', '\\x1b') and not input_buffer:
                break
            elif key.isdigit():
                input_buffer += key
            elif key in ('\\x7f', '\\b', '\\x08'): # Backspace
                input_buffer = input_buffer[:-1]
            elif key == 'n' and not input_buffer:
                print(f"\\n{Colors.GREEN}{_t('new_msg')}{Colors.RESET}\\n")
                execute_new_session()
                break
            elif key == '\\x1b[A': # UP
                if selected_idx > 0:
                    selected_idx -= 1
                elif page > 1:
                    page -= 1
                    selected_idx = limit - 1
            elif key == '\\x1b[B': # DOWN
                if selected_idx < len(displayed_sessions) - 1:
                    selected_idx += 1
                elif page < total_pages:
                    page += 1
                    selected_idx = 0
            elif key == '\\x1b[C' or (key == '>' and not input_buffer): # RIGHT
                if page < total_pages:
                    page += 1
                    selected_idx = 0
            elif key == '\\x1b[D' or (key == '<' and not input_buffer): # LEFT
                if page > 1:
                    page -= 1
                    selected_idx = 0
            elif key in ('\\n', '\\r'): # ENTER
                if input_buffer:
                    idx = int(input_buffer) - 1
                    input_buffer = "" # reset for next loop if invalid
                else:
                    idx = start_idx + selected_idx
                    
                if 0 <= idx < total_count:
                    if interactive_delete:
                        ui_delete_session(sessions[idx])
                        sessions = get_sessions(search_query=args.search)
                        total_count = len(sessions)
                        if not sessions:
                            break
                    else:
                        print(f"\\n{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+sessions[idx]['id']+Colors.RESET)}\\n")
                        execute_resume_session(sessions[idx]['id'])
                        break
        except (KeyboardInterrupt, EOFError):
            print(f"\\n{Colors.DIM}{_t('cancelled')}{Colors.RESET}")
            break
"""

start_str = "    while True:\n        total_pages = "
parts = content.split(start_str)

new_content = parts[0] + new_loop.strip('\n') + "\n"

with open("agy_sessions/cli.py", "w") as f:
    f.write(new_content)
