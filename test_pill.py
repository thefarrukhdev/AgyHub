idx = "1"
relative = "1 soat oldin"
id_tag = "b000caf4"
prompt = "hullas meni git hubimni"

bg = "\033[48;5;39m"  # Blue background
fg_black = "\033[38;5;232m" # Black text
fg_blue = "\033[38;5;39m"  # Blue foreground
reset = "\033[0m"

pill_left = f"{fg_blue}{bg}{fg_black}"
pill_right = f"{reset}{fg_blue}{reset}"

# Pad exactly 113 chars (approximate table width)
content = f"{idx:<3} │ {relative:<14} │ {id_tag:<20} │ {prompt}".ljust(113)

print(f"  {pill_left}{content}{pill_right}")
