import os
import json
import subprocess
import shutil

TOKEN_FILE = os.path.expanduser("~/.gemini/oauth_tokens.json")

def get_saved_accounts():
    if not os.path.exists(TOKEN_FILE):
        return []
    try:
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
            return list(tokens.keys())
    except Exception:
        return []

def get_current_account():
    bin_path = shutil.which("agy-oauth-manager")
    if not bin_path:
        return None
    try:
        res = subprocess.run([bin_path, "--current"], capture_output=True, text=True)
        if "ECHO_EMAIL:" in res.stdout:
            return res.stdout.strip().split("ECHO_EMAIL:")[1]
    except Exception:
        pass
    return None

def rotate_account():
    bin_path = shutil.which("agy-oauth-manager")
    if not bin_path:
        return False, "Not installed"
    try:
        res = subprocess.run([bin_path, "--rotate"], capture_output=True, text=True)
        if "ECHO_EMAIL:" in res.stdout:
            return True, res.stdout.strip().split("ECHO_EMAIL:")[1]
        return False, res.stdout
    except Exception as e:
        return False, str(e)

def save_current_account():
    bin_path = shutil.which("agy-oauth-manager")
    if not bin_path:
        return False, "Not installed"
    try:
        res = subprocess.run([bin_path, "--save"], capture_output=True, text=True)
        if "Success" in res.stdout or "✅" in res.stdout:
            return True, "Saved"
        return False, res.stdout
    except Exception as e:
        return False, str(e)

def delete_account(email):
    bin_path = shutil.which("agy-oauth-manager")
    if bin_path:
        try:
            res = subprocess.run([bin_path, "--delete", email], capture_output=True, text=True)
            if res.returncode == 0:
                return True, res.stdout.strip()
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, str(e)
    # Fallback: direct file edit
    if not os.path.exists(TOKEN_FILE):
        return False, "No accounts saved."
    try:
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
        if email in tokens:
            del tokens[email]
            temp_file = f"{TOKEN_FILE}.tmp"
            open(temp_file, 'a').close()
            os.chmod(temp_file, 0o600)
            with open(temp_file, 'w') as f:
                json.dump(tokens, f, indent=4)
            os.replace(temp_file, TOKEN_FILE)
            return True, f"Account {email} deleted."
        return False, "Account not found."
    except Exception as e:
        return False, str(e)
