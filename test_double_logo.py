C = "\x1b[38;2;23;147;209m"
R = "\x1b[m"
arch_logo = [
    f"    {C}▄▄{R}",
    f"   {C}████{R}",
    f"  {C}██▄▄██{R}",
    f" {C}██{R}    {C}██{R}",
    f"{C}▀██{R}      {C}██▀{R}"
]
for l in arch_logo:
    print(l)
