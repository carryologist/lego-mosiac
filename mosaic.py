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
    
    # Generate LDraw file for BrickLink Studio
    # LDraw colors: 0 = black, 15 = white
    # Part 3024 = 1x1 plate, 3070b = 1x1 tile (flat)
    ldr_filename = f"mosaic_{output_size}x{output_size}.ldr"
    with open(ldr_filename, 'w') as f:
        f.write(f"0 Coder Logo Mosaic {output_size}x{output_size}\n")
        f.write("0 Author: Mux\n")
        f.write("0 !LICENSE Redistributable under CCAL version 2.0\n")
        
        # LDraw units: 1 stud = 20 LDU, plate height = 8 LDU
        # 1x1 tile origin is at center, so offset by 10 LDU (half stud)
        stud = 20
        for y in range(output_size):
            for x in range(output_size):
                color = 15 if pixels[x, y] > threshold else 0  # white or black
                # Position: center of each stud position
                lx = (x * stud) + 10
                lz = (y * stud) + 10
                # 1 = line type for part, identity matrix for no rotation
                f.write(f"1 {color} {lx} 0 {lz} 1 0 0 0 1 0 0 0 1 3070b.dat\n")
        
        f.write("0 STEP\n")
    
    print(f"LDraw file saved to: {ldr_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mosaic.py <image_path> [size]")
        sys.exit(1)
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    create_mosaic(sys.argv[1], size)
