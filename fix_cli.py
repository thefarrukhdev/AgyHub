with open("agy_sessions/cli.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "if key in ('q', 'Q'," in line:
        new_lines.append("            if key in ('q', 'Q', '\\x1b'):\n")
    elif "print(f\"" in line and "{Colors.GREEN}{_t('new_msg')}{Colors.RESET}" in line:
        new_lines.append("                print(f\"\\n{Colors.GREEN}{_t('new_msg')}{Colors.RESET}\\n\")\n")
    elif "print(f\"" in line and "{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+sessions[idx]['id']+Colors.RESET)}" in line:
        new_lines.append("                        print(f\"\\n{Colors.GREEN}{_t('resume_msg', id=Colors.BOLD+sessions[idx]['id']+Colors.RESET)}\\n\")\n")
    elif "print(f\"" in line and "{Colors.DIM}{_t('cancelled')}{Colors.RESET}" in line:
        new_lines.append("            print(f\"\\n{Colors.DIM}{_t('cancelled')}{Colors.RESET}\\n\")\n")
    else:
        new_lines.append(line)

with open("agy_sessions/cli.py", "w") as f:
    f.writelines(new_lines)
