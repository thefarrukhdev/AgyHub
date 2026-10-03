import sys
import argparse
from typing import List, Dict

from agy_sessions.i18n.manager import load_language, _t
from agy_sessions.ui.colors import Colors
from agy_sessions.ui.table import print_beautiful_table
from agy_sessions.core.session import (
    get_sessions,
    resolve_session_selection,
    safe_delete_session,
    execute_resume_session,
    execute_new_session,
    toggle_pin_file,
    write_tag_file
)
from agy_sessions.core.db import invalidate_session, update_session_meta
from agy_sessions.core.input import read_key

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
            
            print(f" {Colors.BOLD}{color}{_t('prompt_enter', actions=prompt_str)}{Colors.RESET} {input_buffer}", end="")
            sys.stdout.flush()
            
            key = read_key()
            
            if key in ('q', 'Q', '\x1b') and not input_buffer:
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
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.DIM}{_t('cancelled')}{Colors.RESET}")
            break
