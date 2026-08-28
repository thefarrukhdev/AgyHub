# 🚀 Antigravity Session Manager

A beautiful, zero-dependency Terminal User Interface (TUI) to view, manage, and seamlessly resume [Google Antigravity (AGY)](https://github.com/google/antigravity) CLI sessions.

![UI Preview](https://img.shields.io/badge/UI-Beautiful_Box_Drawing-cyan)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)
![License](https://img.shields.io/badge/License-MIT-purple)

## ✨ Features

- **Stunning UI**: Beautiful box-drawn terminal tables with modern ANSI colors, giving a native application feel directly in your terminal.
- **Zero Dependencies**: Built entirely using Python's Standard Library. No `rich`, `colorama`, or `pandas` needed. Extremely portable.
- **Smart Parsing**: Automatically extracts and truncates the very first `<USER_REQUEST>` prompt from your AGY `.jsonl` transcript logs to give context to your sessions.
- **Relative Timestamps**: Displays modern, Git-style relative timestamps (e.g., `Just now`, `5 mins ago`, `Yesterday`).
- **Interactive Resume**: Type a number to instantly resume the conversation right where you left off.

## 📦 Installation

Since it's a single Python script with no dependencies, installation is instantaneous.

```bash
# 1. Download the script
curl -O https://raw.githubusercontent.com/FarrukhDev-io/antigravity-session-manager/main/agy-sessions

# 2. Make it executable
chmod +x agy-sessions

# 3. Move it to your local bin (make sure ~/.local/bin is in your PATH)
mv agy-sessions ~/.local/bin/
```

### 💡 Pro Tip (Alias)
For maximum speed, add an alias to your `.bashrc` or `.zshrc`:
```bash
alias chats="agy-sessions"
```
Now you can simply type `chats` anywhere in your terminal to bring up your session history!

## ⚙️ How it Works (For Humans & AI)

The AGY CLI natively stores conversation logs inside `~/.gemini/antigravity-cli/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`. 

This script iterates through the `brain/` directory, safely parses the latest `transcript.jsonl` files line-by-line without loading the entire massive file into memory, and extracts the `USER_INPUT` event block. It then cleans XML tags (like `<USER_REQUEST>`) to show a clean prompt preview. 

Once a user selects an index, the script utilizes `os.execvp()` to perfectly hand over the terminal process to `agy --conversation <id>`, ensuring smooth context restoration.

## 📜 License

MIT License. Do whatever you want with it! Built for the developer community.
