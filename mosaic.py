#!/usr/bin/env python3
"""Convert Coder logo to 32x32 LEGO mosaic."""

from PIL import Image
import sys

def create_mosaic(input_path, output_size=32):
    # Load and resize
    img = Image.open(input_path).convert('L')  # Grayscale
    img = img.resize((output_size, output_size), Image.Resampling.LANCZOS)
    
    # Threshold to black/white
    threshold = 128
    pixels = img.load()
    
    black_count = 0
    white_count = 0
    
    # Create output image for preview
    preview = Image.new('RGB', (output_size, output_size))
    preview_pixels = preview.load()
    
    print(f"\n32x32 Mosaic Grid (# = white, . = black):\n")
    
    for y in range(output_size):
        row = ""
        for x in range(output_size):
            if pixels[x, y] > threshold:
                row += "# "
                preview_pixels[x, y] = (255, 255, 255)
                white_count += 1
            else:
                row += ". "
                preview_pixels[x, y] = (0, 0, 0)
                black_count += 1
        print(row)
    
    # Save preview (scaled up for visibility)
    preview_large = preview.resize((512, 512), Image.Resampling.NEAREST)
    preview_large.save('mosaic_preview.png')
    
    print(f"\n--- Parts List ---")
    print(f"Black 1x1 plates/tiles: {black_count}")
    print(f"White 1x1 plates/tiles: {white_count}")
    print(f"Total pieces: {black_count + white_count}")
    print(f"\nPreview saved to: mosaic_preview.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mosaic.py <image_path> [size]")
        sys.exit(1)
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    create_mosaic(sys.argv[1], size)
