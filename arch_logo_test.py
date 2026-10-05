def print_arch():
    C = "\033[38;2;23;147;209m" # Arch Blue
    R = "\033[0m"
    
    logo = [
        f"      {C}▄▄{R}      ",
        f"     {C}████{R}     ",
        f"    {C}██{R}  {C}██{R}    ",
        f"   {C}██{R}    {C}██{R}   ",
        f"  {C}██▀{R}      {C}▀██{R}  "
    ]
    for l in logo: print(l)

print_arch()
