def print_logo(logo):
    for l in logo: print(l)
    print("-" * 20)

C = "\x1b[38;2;23;147;209m"
R = "\x1b[m"

logo1 = [
    f"     {C}▄▄{R}",
    f"    {C}████{R}",
    f"   {C}██████{R}",
    f"  {C}██▀▄▄▀██{R}",
    f" {C}██▀{R}    {C}▀██{R}"
]

logo2 = [
    f"     {C}▄▄{R}",
    f"    {C}████{R}",
    f"   {C}██████{R}",
    f"  {C}███▄▄███{R}",
    f"  {C}█▀{R}    {C}▀█{R}"
]

logo3 = [
    f"      {C}▄{R}",
    f"     {C}███{R}",
    f"    {C}█████{R}",
    f"   {C}██▀ ▀██{R}",
    f"  {C}█▀{R}     {C}▀█{R}"
]

logo4 = [
    f"      {C}▄{R}",
    f"     {C}▟█▙{R}",
    f"    {C}▟███▙{R}",
    f"   {C}▟██{R} {C}██▙{R}",
    f"  {C}▟█▀{R}   {C}▀█▙{R}"
]

logo5 = [
    f"     {C}▄▄{R}",
    f"    {C}▟██▙{R}",
    f"   {C}▟████▙{R}",
    f"  {C}▟██▀▀██▙{R}",
    f" {C}▟█▀{R}    {C}▀█▙{R}"
]

for i, l in enumerate([logo1, logo2, logo3, logo4, logo5]):
    print(f"Logo {i+1}:")
    print_logo(l)

