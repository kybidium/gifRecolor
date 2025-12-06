import json
import numpy as np
from PIL import Image
import sys
import os

def recolor_gif(input_path, output_path, replacements_path):
    print(f"Opening {input_path}...")
    try:
        img = Image.open(input_path)
    except IOError:
        print(f"Error: Could not open {input_path}")
        return

    print(f"Loading replacements from {replacements_path}...")
    try:
        with open(replacements_path, 'r') as f:
            replacements_list = json.load(f)
    except IOError:
        print(f"Error: Could not open {replacements_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {replacements_path}")
        return

    # Convert list of pairs to a dictionary for easier lookup
    # Expecting format: [[r1, g1, b1], [r2, g2, b2]]
    # We'll use a dictionary mapping tuple(old_color) -> tuple(new_color)
    replacements = {}
    for item in replacements_list:
        if len(item) == 2:
            old_color = tuple(item[0])
            new_color = tuple(item[1])
            replacements[old_color] = new_color

    print(f"Loaded {len(replacements)} replacements.")

    frames = []
    try:
        while True:
            frames.append(img.copy().convert('RGB'))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    
    print(f"Processing {len(frames)} frames...")

    new_frames = []
    for frame in frames:
        data = np.array(frame)
        h, w, c = data.shape
        pixels = data.reshape((-1, 3))
        
        # Create a new array for modified pixels
        new_pixels = pixels.copy()
        
        # Apply replacements
        # This can be optimized, but iterating is simple for now
        for i in range(len(pixels)):
            current_color = tuple(pixels[i])
            if current_color in replacements:
                new_pixels[i] = replacements[current_color]
        
        # Reshape back to image dimensions
        new_data = new_pixels.reshape((h, w, c)).astype(np.uint8)
        
        # Convert back to PIL Image
        new_frame = Image.fromarray(new_data)
        new_frames.append(new_frame)

    # Save the new GIF
    print(f"Saving to {output_path}...")
    new_frames[0].save(
        output_path,
        save_all=True,
        append_images=new_frames[1:],
        duration=img.info.get('duration', 100),
        loop=img.info.get('loop', 0)
    )
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 recolor.py <input_gif> <output_gif> <replacements.json>")
    else:
        recolor_gif(sys.argv[1], sys.argv[2], sys.argv[3])
