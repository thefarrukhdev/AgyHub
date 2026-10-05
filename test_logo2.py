def print_logo():
    # Colors approximation from the image (Google/Antigravity style gradient)
    C1 = "\033[38;5;214m" # Orange
    C2 = "\033[38;5;203m" # Light Red/Pink
    C3 = "\033[38;5;170m" # Purple
    C4 = "\033[38;5;33m"  # Blue
    C5 = "\033[38;5;39m"  # Light Blue
    C6 = "\033[38;5;51m"  # Cyan
    R = "\033[0m"
    
    logo = [
        f"     {C1}██{R}",
        f"    {C2}████{R}",
        f"   {C3}██████{R}",
        f"  {C4}██{R}    {C4}██{R}",
        f" {C5}██{R}      {C5}██{R}",
        f"{C6}██{R}        {C6}██{R}"
    ]
    
    # Text next to logo
    lines = [
        "AgyHub 2.0.0 (Antigravity Sessiya Menejeri)",
        "Jami chatlar: 299 | Sahifa 1/20",
        "",
        "",
        "",
        ""
    ]
    
    for i in range(6):
        print(f"{logo[i]}    {lines[i]}")

print_logo()
