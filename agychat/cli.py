import sys
import argparse
from typing import List, Dict

from agychat.i18n.manager import load_language, _t
from agychat.ui.colors import Colors
from agychat.ui.table import print_beautiful_table
from agychat.core.session import (
    get_sessions,
    resolve_session_selection,
    safe_delete_session,
    execute_resume_session,
    execute_new_session,
    toggle_pin_file,
    write_tag_file
)
from agychat.core.db import invalidate_session, update_session_meta
from agychat.core.input import read_key
from agychat.ui.accounts_table import print_accounts_table
from agychat.core.accounts import get_saved_accounts, get_current_account

def ui_delete_session(session: Dict):
    print(f"\n{Colors.RED}{_t('warn_del_session', id=Colors.BOLD+session['id'][:8]+Colors.RESET)}")
    print(f"{_t('prompt_label', prompt=Colors.DIM+session['prompt']+Colors.RESET)}")
    confirm = input(_t('confirm_del')).strip().lower()
    
    yes_word = _t('yes_word').lower()
    if confirm in ['y', 'yes', yes_word, yes_word[0] if yes_word else 'y']:
        try:
            safe_delete_session(session['path'])
            invalidate_session(session['id'])
            print(f"{Colors.GREEN}{_t('success_del')}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{_t('error_del', e=e)}{Colors.RESET}")
    else:
        print(f"{Colors.DIM}{_t('cancel_del')}{Colors.RESET}")

def ui_clear_all_sessions(sessions: List[Dict]):
    if not sessions:
        print(f"{Colors.YELLOW}{_t('no_sessions_clear')}{Colors.RESET}")
        return
        
    print(f"\n{Colors.RED}{_t('warn_del_all', n=len(sessions))}{Colors.RESET}")
    yes_word = _t('yes_word')
    confirm = input(_t('confirm_del_all', yes=yes_word)).strip()
    
    if confirm == yes_word:
        count = 0
        for s in sessions:
            try:
                safe_delete_session(s['path'])
                invalidate_session(s['id'])
                count += 1
            except Exception as e:
                print(f"{Colors.RED}{_t('error_del_id', id=s['id'][:8], e=e)}{Colors.RESET}")
        print(f"{Colors.GREEN}{_t('success_del_all', n=count)}{Colors.RESET}")
    else:
        print(f"{Colors.DIM}{_t('cancel_clear_all')}{Colors.RESET}")

def ui_toggle_pin(session: Dict, pin: bool):
    try:
        toggle_pin_file(session['path'], pin)
        update_session_meta(session['id'], pinned=pin)
        if pin:
            print(f"{Colors.GREEN}{_t('success_pinned', id=session['id'][:8])}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}{_t('success_unpinned', id=session['id'][:8])}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}{_t('error_pin', e=e)}{Colors.RESET}")

def ui_set_tag(session: Dict, tag: str):
    try:
        write_tag_file(session['path'], tag)
        update_session_meta(session['id'], tag=tag)
        if tag:
            print(f"{Colors.GREEN}{_t('success_tagged', id=session['id'][:8], tag=tag)}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}{_t('success_untagged', id=session['id'][:8])}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}{_t('error_tag', e=e)}{Colors.RESET}")

def main():
    lang_parser = argparse.ArgumentParser(add_help=False)
    lang_parser.add_argument("--lang")
    lang_args, _ = lang_parser.parse_known_args()
    
    load_language(lang_args.lang)
    
    parser = argparse.ArgumentParser(description=_t('arg_desc'))
    parser.add_argument("select", nargs="?", help=_t('arg_select'))
    parser.add_argument("-n", "--number", type=int, default=15, help=_t('arg_num'))
    parser.add_argument("-p", "--page", type=int, default=1, help=_t('arg_page'))
    parser.add_argument("-s", "--search", type=str, help=_t('arg_search'))
    parser.add_argument("-d", "--delete", action="store_true", help=_t('arg_del'))
    parser.add_argument("-t", "--tag", type=str, help=_t('arg_tag'))
    parser.add_argument("--untag", action="store_true", help=_t('arg_untag'))
    parser.add_argument("--pin", action="store_true", help=_t('arg_pin'))
    parser.add_argument("--unpin", action="store_true", help=_t('arg_unpin'))
    parser.add_argument("--clear-all", action="store_true", help=_t('arg_clear_all'))
    parser.add_argument("--list", action="store_true", help=_t('arg_list'))
    parser.add_argument("--lang", choices=['en', 'ru', 'uz'], help=_t('arg_lang'))
    args = parser.parse_args()

    sessions = get_sessions(search_query=args.search)
    total_count = len(sessions)
    
    if args.clear_all:
        ui_clear_all_sessions(sessions)
        return

    if args.select:
        session = resolve_session_selection(args.select, sessions)
        if not session:
            print(f"{Colors.RED}{_t('error_not_found')}{Colors.RESET}")
            sys.exit(1)
            
        if args.tag is not None or args.untag or args.pin or args.unpin or args.delete:
            if args.tag is not None:
                ui_set_tag(session, args.tag)
            if args.untag:
                ui_set_tag(session, "")
            if args.pin:
                ui_toggle_pin(session, True)
            if args.unpin:
                ui_toggle_pin(session, False)
            if args.delete:
                ui_delete_session(session)
            return
            
        print(f"\n{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+session['id']+Colors.RESET)}\n")
        execute_resume_session(session['id'])
        return

    if not sessions:
        if args.search:
            print(f"{Colors.YELLOW}{_t('no_sessions_search', search=args.search, count=total_count)}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{_t('no_sessions')}{Colors.RESET}")
        
        choice = input(f"\n{Colors.MAGENTA}{_t('prompt_new')}{Colors.RESET}").strip().lower()
        if choice == 'n':
            print(f"\n{Colors.GREEN}{_t('new_msg')}{Colors.RESET}\n")
            execute_new_session()
        sys.exit(0)

    page = args.page
    limit = args.number if args.number > 0 else total_count
    interactive_delete = args.delete
    action_text = _t('action_delete') if interactive_delete else _t('action_resume')
    color = Colors.RED if interactive_delete else Colors.MAGENTA

    selected_idx = 0


    view_mode = "CHATS"
    is_searching = False
    accounts_selected_idx = 0
    selected_idx = 0
    input_buffer = ""
    current_search_query = args.search or ""

    while True:
        if view_mode == "CHATS":
            sessions = get_sessions(search_query=current_search_query)
            total_count = len(sessions)
            total_pages = (total_count + limit - 1) // limit if limit > 0 else 1
            page = max(1, min(page, total_pages)) if total_pages > 0 else 1
            
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            displayed_sessions = sessions[start_idx:end_idx]
            
            if selected_idx >= len(displayed_sessions):
                selected_idx = max(0, len(displayed_sessions) - 1)
            if selected_idx < 0:
                selected_idx = 0

            print_beautiful_table(displayed_sessions, total_count=total_count, start_idx=start_idx, page=page, total_pages=total_pages, search_query=current_search_query, selected_idx=selected_idx)

            try:
                if is_searching:
                    print(f" {Colors.BOLD}{Colors.CYAN}Search 🔍 : {Colors.RESET}{input_buffer}", end="")
                else:
                    print(f" {Colors.BOLD}{color}▶ {Colors.RESET}{input_buffer}", end="")
                import sys
                sys.stdout.flush()
                
                key = read_key()
                
                if is_searching:
                    if key == '\x1b': # ESC
                        is_searching = False
                        input_buffer = ""
                        current_search_query = args.search or ""
                    elif key in ('\n', '\r'):
                        is_searching = False
                        current_search_query = input_buffer
                        input_buffer = ""
                    elif key in ('\x7f', '\b', '\x08'):
                        input_buffer = input_buffer[:-1]
                        current_search_query = input_buffer
                    elif len(key) == 1 and not key.startswith('\x1b'):
                        input_buffer += key
                        current_search_query = input_buffer
                    continue

                if key == '\t':
                    view_mode = "ACCOUNTS"
                    continue
                elif key == 'a' and not input_buffer:
                    view_mode = "ACCOUNTS"
                    continue
                elif key == 's' and not input_buffer:
                    is_searching = True
                    input_buffer = ""
                    continue
                elif key == 't' and not input_buffer:
                    if displayed_sessions:
                        sess = displayed_sessions[selected_idx]
                        print(f"\n{Colors.CYAN}Enter new tag for {sess['id'][:8]} (leave empty to remove): {Colors.RESET}", end="")
                        sys.stdout.flush()
                        tag_input = input().strip()
                        ui_set_tag(sess, tag_input)
                        import time
                        time.sleep(0.5)
                    continue
                elif key == 'p' and not input_buffer:
                    if displayed_sessions:
                        sess = displayed_sessions[selected_idx]
                        ui_toggle_pin(sess, not sess.get('pinned'))
                        import time
                        time.sleep(0.5)
                    continue
                elif key in ('q', 'Q', '\x1b') and not input_buffer:
                    break
                elif key.isdigit():
                    input_buffer += key
                elif key in ('\x7f', '\b', '\x08'): # Backspace
                    input_buffer = input_buffer[:-1]
                elif key == 'n' and not input_buffer:
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
                elif key == '\x1b[C' or (key == '>' and not input_buffer): # RIGHT
                    if page < total_pages:
                        page += 1
                        selected_idx = 0
                elif key == '\x1b[D' or (key == '<' and not input_buffer): # LEFT
                    if page > 1:
                        page -= 1
                        selected_idx = 0
                elif key in ('\n', '\r'): # ENTER
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
                            print(f"\n{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+sessions[idx]['id']+Colors.RESET)}\n")
                            execute_resume_session(sessions[idx]['id'])
                            break
                elif key == '?':
                    print(f"\n{Colors.BOLD}{Colors.CYAN}AgyChat Help Menu{Colors.RESET}\n")
                    print(f"  {Colors.BOLD}[↑ / ↓]{Colors.RESET} Navigate up and down")
                    print(f"  {Colors.BOLD}[ Enter ]{Colors.RESET} Resume selected session")
                    print(f"  {Colors.BOLD}[  s  ]{Colors.RESET} Live search through prompts and tags")
                    print(f"  {Colors.BOLD}[  t  ]{Colors.RESET} Add or remove a tag from a session")
                    print(f"  {Colors.BOLD}[  p  ]{Colors.RESET} Pin or unpin a session")
                    print(f"  {Colors.BOLD}[  a  ]{Colors.RESET} Open Account Manager (Rotate, Save, Status)")
                    print(f"  {Colors.BOLD}[  q  ]{Colors.RESET} Quit the application\n")
                    print(f"{Colors.DIM}Press any key to return...{Colors.RESET}")
                    sys.stdout.flush()
                    read_key()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Colors.DIM}{_t('cancelled')}{Colors.RESET}")
                break
        elif view_mode == "ACCOUNTS":
            saved = get_saved_accounts()
            curr = get_current_account()
            if accounts_selected_idx >= len(saved):
                accounts_selected_idx = max(0, len(saved) - 1)
            if accounts_selected_idx < 0:
                accounts_selected_idx = 0
            
            print_accounts_table(saved, curr, accounts_selected_idx)
            
            print(f" {Colors.BOLD}{Colors.CYAN}Accounts ⚙️ : {Colors.RESET}{Colors.DIM}[Enter] Switch  |  [a] Add  |  [d] Delete  |  [c] Limits  |  [Tab] Back{Colors.RESET} ", end="")
            import sys
            sys.stdout.flush()
            
            try:
                key = read_key()
                if key == '\t':
                    view_mode = "CHATS"
                    continue
                elif key == '\x1b[A': # UP
                    if accounts_selected_idx > 0:
                        accounts_selected_idx -= 1
                elif key == '\x1b[B': # DOWN
                    if accounts_selected_idx < len(saved) - 1:
                        accounts_selected_idx += 1
                elif key == 's':
                    import subprocess, shutil, time
                    bin_path = shutil.which("agy-oauth-manager")
                    if bin_path:
                        print(f"\n{Colors.CYAN}Saving current account...{Colors.RESET}")
                        subprocess.run([bin_path, "--save"])
                        time.sleep(1.5)
                elif key == 'c':
                    import subprocess, shutil
                    bin_path = shutil.which("agy-oauth-manager")
                    if bin_path:
                        print(f"\n{Colors.CYAN}Checking account limits...{Colors.RESET}")
                        subprocess.run([bin_path, "--status"])
                        print(f"\n{Colors.DIM}Press any key to return...{Colors.RESET}")
                        sys.stdout.flush()
                        read_key()
                elif key == 'd':
                    if len(saved) > 0 and 0 <= accounts_selected_idx < len(saved):
                        email_to_del = saved[accounts_selected_idx]
                        print(f"\n{Colors.RED}Are you sure you want to delete {Colors.BOLD}{email_to_del}{Colors.RESET}{Colors.RED}? (y/N): {Colors.RESET}", end="")
                        sys.stdout.flush()
                        confirm = input().strip().lower()
                        if confirm == 'y':
                            from agychat.core.accounts import delete_account
                            delete_account(email_to_del)
                            print(f"{Colors.GREEN}Account {email_to_del} deleted.{Colors.RESET}")
                            import time
                            time.sleep(1)
                elif key == 'a':
                    import subprocess, shutil, time
                    bin_path = shutil.which("agy-oauth-manager")
                    if not bin_path:
                        print(f"\n{Colors.RED}agy-oauth-manager not found in PATH.{Colors.RESET}")
                        print(f"{Colors.DIM}Press any key to continue...{Colors.RESET}")
                        sys.stdout.flush()
                        read_key()
                    else:
                        print(f"\n{Colors.BOLD}{Colors.CYAN}═══ Add New Account ═══{Colors.RESET}")
                        print(f"{Colors.YELLOW}Steps:{Colors.RESET}")
                        print(f"  1. Open Antigravity IDE (or CLI in another terminal) and sign in")
                        print(f"  2. Come back here and press {Colors.BOLD}[Enter]{Colors.RESET} to save that account")
                        print(f"  3. Or press {Colors.BOLD}[Esc]{Colors.RESET} to cancel")
                        print(f"\n{Colors.DIM}Waiting for you...{Colors.RESET} ", end="")
                        sys.stdout.flush()
                        confirm_key = read_key()
                        if confirm_key in ('\n', '\r'):
                            print(f"\n{Colors.CYAN}Saving account...{Colors.RESET}")
                            sys.stdout.flush()
                            result = subprocess.run([bin_path, "--save"], capture_output=True, text=True)
                            if result.returncode == 0:
                                print(f"{Colors.GREEN}{result.stdout.strip()}{Colors.RESET}")
                            else:
                                print(f"{Colors.RED}{result.stderr.strip() or result.stdout.strip()}{Colors.RESET}")
                            time.sleep(2)
                        else:
                            print(f"\n{Colors.DIM}Cancelled.{Colors.RESET}")
                            time.sleep(0.5)
                elif key in ('\n', '\r'):
                    if len(saved) > 0 and 0 <= accounts_selected_idx < len(saved):
                        email_to_switch = saved[accounts_selected_idx]
                        import subprocess, shutil, time
                        bin_path = shutil.which("agy-oauth-manager")
                        if bin_path:
                            print(f"\n{Colors.CYAN}Switching to {email_to_switch}...{Colors.RESET}")
                            import sys
                            sys.stdout.flush()
                            subprocess.run([bin_path, "--switch", email_to_switch])
                            time.sleep(1)
                elif key.isdigit():
                    idx = int(key) - 1
                    if len(saved) > 0 and 0 <= idx < len(saved):
                        email_to_switch = saved[idx]
                        import subprocess, shutil, time
                        bin_path = shutil.which("agy-oauth-manager")
                        if bin_path:
                            print(f"\n{Colors.CYAN}Switching to {email_to_switch}...{Colors.RESET}")
                            import sys
                            sys.stdout.flush()
                            subprocess.run([bin_path, "--switch", email_to_switch])
                            time.sleep(1)
                elif key in ('q', 'Q', '\x1b'):
                    break
            except (KeyboardInterrupt, EOFError):
                break
