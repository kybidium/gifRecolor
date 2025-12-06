import numpy as np
from PIL import Image
""" FOR DEBUGGING GIF COLORS """
def analyze_gif_colors(gif_path):
    print(f"Analyzing colors in {gif_path}...")
    try:
        img = Image.open(gif_path)
    except IOError:
        print(f"Error: Could not open {gif_path}")
        return

    all_colors = set()
    
    try:
        while True:
            # Convert to RGB to get actual colors
            frame = img.copy().convert('RGB')
            # Get unique colors
            colors = frame.getcolors(maxcolors=1000000)
            if colors:
                for count, color in colors:
                    all_colors.add(color)
            img.seek(img.tell() + 1)
    except EOFError:
        pass
        
    print(f"Found {len(all_colors)} unique colors:")
    for color in sorted(list(all_colors)):
        print(color)

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_colors.py <input_gif>")
        print("Running with default: outputs/mochicat_kmeans.gif")
        analyze_gif_colors("outputs/mochicat_kmeans.gif")
    else:
        analyze_gif_colors(sys.argv[1])
