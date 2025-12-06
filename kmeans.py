import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import os

def process_gif(input_path, output_path, n_clusters=6):
    """
    Reads a GIF, applies k-means clustering to the pixel colors,
    and saves the recolored GIF.
    """
    print(f"Opening {input_path}...")
    try:
        img = Image.open(input_path)
    except IOError:
        print(f"Error: Could not open {input_path}")
        return

    frames = []
    try:
        while True:
            frames.append(img.copy().convert('RGB'))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    
    print(f"Extracted {len(frames)} frames.")

    # Collect all pixels from all frames to find global centroids
    all_pixels = []
    for frame in frames:
        # Convert frame to numpy array
        data = np.array(frame)
        # Reshape to (num_pixels, 3)
        pixels = data.reshape((-1, 3))
        all_pixels.append(pixels)
    
    # Concatenate all pixels
    all_pixels = np.concatenate(all_pixels, axis=0)
    
    print(f"Training KMeans with k={n_clusters} on {all_pixels.shape[0]} pixels...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(all_pixels)
    centroids = kmeans.cluster_centers_.astype(int)
    print(f"Centroids found: {centroids}")

    # Save centroids to file
    centroids_path = output_path.replace('.gif', '_centroids.txt')
    print(f"Saving centroids to {centroids_path}...")
    with open(centroids_path, 'w') as f:
        f.write(f"{input_path}\n")
        for centroid in centroids:
            f.write(f"{centroid[0]}, {centroid[1]}, {centroid[2]}\n")

    # Reconstruct frames
    new_frames = []
    print("Recoloring frames...")
    for frame in frames:
        data = np.array(frame)
        h, w, c = data.shape
        pixels = data.reshape((-1, 3))
        
        # Predict clusters for all pixels in the frame
        labels = kmeans.predict(pixels)
        
        # Replace pixel values with centroid values
        new_pixels = centroids[labels]
        
        # Reshape back to image dimensions
        new_data = new_pixels.reshape((h, w, c)).astype(np.uint8)
        
        # Convert back to PIL Image
        new_frame = Image.fromarray(new_data)
        new_frames.append(new_frame)

    # Save the new GIF
    print(f"Saving to {output_path}...")
    # Save the first frame as the GIF, appending the rest
    new_frames[0].save(
        output_path,
        save_all=True,
        append_images=new_frames[1:],
        duration=img.info.get('duration', 100),
        loop=img.info.get('loop', 0)
    )
    print("Done!")

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 kmeans.py <input_gif> <output_gif> [n_clusters]")
        # Fallback to default for convenience if running without args during dev, 
        # but user specifically asked for this structure so maybe I should just print usage.
        # I'll keep the default behavior if no args are passed but print usage info.
        print("Running with default values...")
        input_gif = "data/mochicat.gif"
        output_gif = "outputs/mochicat_kmeans.gif"
        n_clusters = 6
    else:
        input_gif = sys.argv[1]
        output_gif = sys.argv[2]
        n_clusters = int(sys.argv[3]) if len(sys.argv) > 3 else 6

    if os.path.exists(input_gif):
        process_gif(input_gif, output_gif, n_clusters)
    else:
        print(f"File not found: {input_gif}")