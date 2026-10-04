with open("README.md", "r") as f:
    content = f.read()

old_install = """## 📦 Installation

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
Now you can simply type `chats` anywhere in your terminal to open AgyHub!"""

new_install = """## 📦 Installation

We officially support installation via modern Python tool managers like `uv` or `pipx`.

```bash
# 1. Clone the repository
git clone https://github.com/thefarrukhdev/AgyHub.git
cd AgyHub

# 2. Install using uv (or pipx)
uv tool install .
```

That's it! Installing via `uv` or `pipx` automatically adds **three** command aliases to your terminal. You can run the tool using any of them:
- `agyhub`
- `chats`
- `agy-sessions`"""

content = content.replace(old_install, new_install)

with open("README.md", "w") as f:
    f.write(content)
