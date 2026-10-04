with open("pyproject.toml", "r") as f:
    content = f.read()

old_scripts = """[project.scripts]
agy-sessions = "agy_sessions.cli:main\""""

new_scripts = """[project.scripts]
agy-sessions = "agy_sessions.cli:main"
agyhub = "agy_sessions.cli:main"
chats = "agy_sessions.cli:main\""""

content = content.replace(old_scripts, new_scripts)

with open("pyproject.toml", "w") as f:
    f.write(content)
