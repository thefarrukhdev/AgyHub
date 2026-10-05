with open("agy_sessions/ui/table.py", "r") as f:
    content = f.read()

bad_block = """    for i in range(7):
        print(f" {arch_logo[i]}{pads_arch[i]}{logo[i]}{pads_logo[i]}    {text_lines[i]}")
    print()"""

content = content.replace(bad_block, "")

with open("agy_sessions/ui/table.py", "w") as f:
    f.write(content)
