import sys
from PIL import Image, ImageDraw, ImageFont
import os

def create_palette_image(centroids_path, output_path):
    print(f"Reading centroids from {centroids_path}...")
    colors = []
    try:
        with open(centroids_path, 'r') as f:
            lines = f.readlines()
            # Skip the first line (filename)
            for line in lines[1:]:
                if line.strip():
                    parts = line.strip().split(',')
                    color = tuple(map(int, parts))
                    colors.append(color)
    except IOError:
        print(f"Error: Could not read {centroids_path}")
        return

    if not colors:
        print("No colors found.")
        return

    # Settings for the palette image
    swatch_size = 100
    padding = 20
    text_height = 40
    
    img_width = (swatch_size + padding) * len(colors) + padding
    img_height = swatch_size + text_height + 2 * padding
    
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        # This is a common path on macOS
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except IOError:
        font = ImageFont.load_default()

    x = padding
    y = padding
    
    for color in colors:
        # Draw color swatch
        draw.rectangle([x, y, x + swatch_size, y + swatch_size], fill=color, outline='black')
        
        # Draw text label
        text = f"{color[0]},{color[1]},{color[2]}"
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = x + (swatch_size - text_w) / 2
        text_y = y + swatch_size + 5
        
        draw.text((text_x, text_y), text, fill='black', font=font)
        
        x += swatch_size + padding

    print(f"Saving palette to {output_path}...")
    img.save(output_path)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default usage for this project
        default_input = "outputs/mochicat_kmeans_centroids.txt"
        default_output = "outputs/palette.png"
        if os.path.exists(default_input):
            create_palette_image(default_input, default_output)
        else:
            print("Usage: python3 visualize_palette.py <centroids_file> [output_image]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "palette.png"
        create_palette_image(input_file, output_file)
