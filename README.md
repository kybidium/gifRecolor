# gifRecolor

A collection of scripts to recolor GIFs using k-means clustering and color replacements.

## Preprocessing
K-means clustering is used to find the most representative colors in the gif, then the colors in the gif are replaced with the closest colors found by k-means.

## Color replacement
With the colors found by k-means, the new colors in the gif are replaced with colors as specified in the replacements.json file.
