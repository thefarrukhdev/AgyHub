import json
import re
import shutil
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from agychat.core.config import BRAIN_DIR
from agychat.i18n.manager import _t

def get_relative_time(mtime: float) -> str:
    """Convert a timestamp into a human-readable relative time format."""
    diff = datetime.now() - datetime.fromtimestamp(mtime)
    if diff < timedelta(minutes=1):
        return _t('just_now')
    if diff < timedelta(hours=1):
        return _t('min_ago', n=diff.seconds // 60)
    if diff < timedelta(days=1):
        return _t('hrs_ago', n=diff.seconds // 3600)
    if diff < timedelta(days=2):
        return _t('yesterday')
    return _t('days_ago', n=diff.days)

def extract_user_prompt(log_file: Path) -> str:
    """Safely and efficiently extract the first meaningful user prompt from a session log file."""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '"USER_INPUT"' not in line:
                    continue
                
                try:
                    data = json.loads(line)
                    if data.get('type') == 'USER_INPUT':
                        content = data.get('content', '')
                        
                        if isinstance(content, dict):
                            content_str = content.get('text', '')
                        elif isinstance(content, list):
                            content_str = ' '.join(str(c) for c in content)
                        else:
                            content_str = str(content)
                        
                        match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', content_str, re.DOTALL)
                        prompt_text = match.group(1).strip() if match else content_str.strip()

                        prompt_text = re.sub(r'<[^>]+>', '', prompt_text)
                        clean_prompt = ' '.join(prompt_text.split())
                        
                        if clean_prompt:
                            return clean_prompt
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass
    return _t('prompt_no_prompt')

def get_sessions(search_query: str = "") -> List[Dict]:
    """Fetch sessions from the SQLite cache (fast startup sync + DB query)."""
    from agychat.core.db import sync_cache, query_sessions  # late import avoids circular

    # Run the lightweight filesystem sync on every call so that mutations
    # (delete, tag, pin) made outside this process are always reflected.
    sync_cache()

    cached = query_sessions(search_query=search_query)

    sessions = []
    for row in cached:
        sid = row['id']
        conv_dir = BRAIN_DIR / sid
        sessions.append({
            'id':       sid,
            'mtime':    row['mtime'],
            'relative': get_relative_time(row['mtime']),
            'prompt':   row['prompt'],
            'path':     conv_dir,
            'pinned':   row['pinned'],
            'tag':      row['tag'],
        })

    return sessions

def safe_delete_session(path: Path):
    """Delete a session, handling symlinks correctly."""
    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)

def toggle_pin_file(session_path: Path, pin: bool):
    pin_file = session_path / '.agy_pinned'
    if pin:
        pin_file.touch()
    else:
        if pin_file.exists():
            pin_file.unlink()

def write_tag_file(session_path: Path, tag: str):
    tag_file = session_path / '.agy_tag'
    if tag:
        tag_file.write_text(tag, encoding='utf-8')
    else:
        if tag_file.exists():
            tag_file.unlink()

def resolve_session_selection(select_str: str, sessions: List[Dict]) -> Optional[Dict]:
    """Resolve a user input string (index or ID) to a session."""
    for s in sessions:
        if s['id'] == select_str:
            return s
            
    if select_str.isdigit():
        idx = int(select_str) - 1
        if 0 <= idx < len(sessions):
            return sessions[idx]
            
    for s in sessions:
        if s['id'].startswith(select_str):
            return s
            
    return None


def _run_agy_with_retry(cmd: List[str]):
    import subprocess
    import shutil
    import sys
    from agychat.ui.colors import Colors

    bin_path = shutil.which("agy-oauth-manager")
    
    while True:
        # Run agy in the foreground, inheriting stdin/stdout for TTY
        result = subprocess.run(cmd)
        
        # If exit code is 0, it means normal exit (user typed exit, or clean stop)
        if result.returncode == 0:
            break
            
        # Non-zero exit code: possible quota error (429) or other crash.
        if bin_path:
            print(f"\n{Colors.DIM}Session ended with an error (e.g., Quota Exhausted).{Colors.RESET}")
            print(f"{Colors.YELLOW}Checking for other accounts with limits...{Colors.RESET}")
            
            res = subprocess.run([bin_path, "--auto-switch"], capture_output=True, text=True)
            if res.returncode == 0:
                out_msg = res.stdout.strip()
                if out_msg:
                    print(f"\n{Colors.GREEN}✨ {out_msg}{Colors.RESET}")
                    print(f"{Colors.CYAN}Automatically resuming session...{Colors.RESET}\n")
                    import time
                    time.sleep(1)
                    continue
                else:
                    # Current account was fine, so it wasn't a quota error. Just break.
                    break
            else:
                print(f"{Colors.RED}❌ All accounts have exhausted their limits.{Colors.RESET}")
                break
        else:
            break

def execute_resume_session(session_id: str):
    _run_agy_with_retry(["agy", "--conversation", session_id])

def execute_new_session():
    _run_agy_with_retry(["agy"])
