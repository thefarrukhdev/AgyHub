import urllib.request
from PIL import Image
import io

url = "https://raw.githubusercontent.com/archlinux/archlinux-artwork/master/logos/archlinux-logo-dark-scalable.svg"
# Wait, SVG can't be opened directly by PIL without cairo.
# Let's use a PNG from GitHub.
url = "https://raw.githubusercontent.com/neofetch-community/neofetch/master/logo.png" # Not an arch logo

