<div align="center">

# 🚀 AgyHub 
### The Ultimate Antigravity Session Manager

A beautiful, zero-dependency Terminal User Interface (TUI) to view, manage, and seamlessly resume [Google Antigravity (AGY)](https://github.com/google/antigravity) CLI sessions.

<img src="assets/screenshot.png" alt="AgyHub Screenshot" width="800"/>

[![UI Preview](https://img.shields.io/badge/UI-Beautiful_Box_Drawing-cyan)](#)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](#)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](#)
[![License](https://img.shields.io/badge/License-MIT-purple)](#)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

---

## ✨ Features

- **🌍 Multilingual (i18n)**: Fully supports English (`en`), Russian (`ru`), and Uzbek (`uz`). Auto-detects your system language or can be set manually via `--lang`.
- **🎨 Stunning UI**: Beautiful box-drawn terminal tables with modern ANSI colors. Dynamically sized to prevent text-wrapping issues across different languages.
- **⚡ Zero Dependencies**: Built entirely using Python's Standard Library. No external packages needed. Extremely portable.
- **🚀 Lightning Fast**: Optimized lazy-parsing of massive `.jsonl` transcript logs. It reads only what's necessary, making it blazing fast even with hundreds of sessions.
- **🏷️ Tagging & 📌 Pinning**: Give custom names to your important sessions (`--tag`) and pin them to the top of the list (`--pin`).
- **🕹️ Interactive Management**: Type a number to instantly resume a conversation, `n` to start a new one, or navigate through pages (`<`, `>`).
- **🔍 Deep Search**: Instantly find past sessions by searching through prompts or custom tags (`--search`).

## 📦 Installation

Since it's built cleanly, installation takes just seconds.

```bash
# 1. Clone the repository
git clone https://github.com/thefarrukhdev/AgyHub.git
cd AgyHub

# 2. Link the executable to your local bin (make sure ~/.local/bin is in your PATH)
ln -s $(pwd)/agy-sessions ~/.local/bin/agy-sessions
```

### 💡 Pro Tip (Alias)
For maximum speed, add an alias to your `.bashrc` or `.zshrc`:
```bash
alias chats="agy-sessions"
```
Now you can simply type `chats` anywhere in your terminal to open AgyHub!

## 🛠️ Usage

```bash
chats                # Open the interactive UI
chats 5              # Resume session #5 immediately
chats --lang uz      # Switch the UI to Uzbek permanently
chats -t "Backend" 3 # Assign the name "Backend" to session #3
chats --pin 3        # Pin session #3 to the top
chats -s "react"     # Search for "react" in your history
chats --clear-all    # Safely clear all history
```

## ⚙️ Architecture

AgyHub follows strict **SOLID** and **DRY** principles, modularized into a professional package structure:
- `core/` — Handles lazy file I/O, state management, configuration, and robust path resolution.
- `ui/` — Terminal rendering, dynamic grid alignment, and ANSI coloring.
- `i18n/` — Zero-dependency robust translation system with automatic OS language fallback.
- `cli.py` — The core command-line argument parser and logic router.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/thefarrukhdev/AgyHub/issues).

## 📜 License

MIT License. Do whatever you want with it! Built for the developer community.
