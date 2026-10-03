import re

with open("agy_sessions/cli.py", "r") as f:
    content = f.read()

# Add import
content = content.replace(
    "from agy_sessions.core.db import invalidate_session, update_session_meta",
    "from agy_sessions.core.db import invalidate_session, update_session_meta\nfrom agy_sessions.core.input import read_key"
)

new_loop = """
    selected_idx = 0

    while True:
        total_pages = (total_count + limit - 1) // limit
        page = max(1, min(page, total_pages)) if total_pages > 0 else 1
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        displayed_sessions = sessions[start_idx:end_idx]
        
        if selected_idx >= len(displayed_sessions):
            selected_idx = len(displayed_sessions) - 1
        if selected_idx < 0:
            selected_idx = 0

        print_beautiful_table(displayed_sessions, total_count=total_count, start_idx=start_idx, page=page, total_pages=total_pages, search_query=args.search, selected_idx=selected_idx)

        try:
            # We don't use input() anymore, just print instructions
            print(f" {Colors.BOLD}{color}Use ⬆/⬇ to navigate, ENTER to {action_text}, 'n' for new session, 'q' to quit.{Colors.RESET}")
            sys.stdout.flush()
            
            key = read_key()
            
            if key in ('q', 'Q', '\x1b'):
                break
            elif key == 'n':
                print(f"\n{Colors.GREEN}{_t('new_msg')}{Colors.RESET}\n")
                execute_new_session()
                break
            elif key == '\x1b[A': # UP
                if selected_idx > 0:
                    selected_idx -= 1
                elif page > 1:
                    page -= 1
                    selected_idx = limit - 1
            elif key == '\x1b[B': # DOWN
                if selected_idx < len(displayed_sessions) - 1:
                    selected_idx += 1
                elif page < total_pages:
                    page += 1
                    selected_idx = 0
            elif key == '\x1b[C': # RIGHT
                if page < total_pages:
                    page += 1
                    selected_idx = 0
            elif key == '\x1b[D': # LEFT
                if page > 1:
                    page -= 1
                    selected_idx = 0
            elif key in ('\n', '\r'): # ENTER
                idx = start_idx + selected_idx
                if 0 <= idx < total_count:
                    if interactive_delete:
                        ui_delete_session(sessions[idx])
                        sessions = get_sessions(search_query=args.search)
                        total_count = len(sessions)
                        if not sessions:
                            break
                    else:
                        print(f"\n{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+sessions[idx]['id']+Colors.RESET)}\n")
                        execute_resume_session(sessions[idx]['id'])
                        break
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.DIM}{_t('cancelled')}{Colors.RESET}")
            break
"""

# Find the start of the while loop
start_str = "    while True:\n        total_pages = "
parts = content.split(start_str)

new_content = parts[0] + new_loop.strip('\n') + "\n"

with open("agy_sessions/cli.py", "w") as f:
    f.write(new_content)
