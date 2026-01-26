#!/usr/bin/env python3
"""Optimize mosaic by replacing 1x1 tiles with larger pieces."""

# Available tile sizes (prioritize larger pieces)
# Format: (width, height, part_number)
TILES = [
    (2, 2, "3068b"),   # 2x2 tile
    (2, 1, "3069b"),   # 1x2 tile
    (1, 2, "3069b"),   # 2x1 tile (same part, rotated)
    (1, 1, "3070b"),   # 1x1 tile
]

def parse_ldr(filename):
    """Parse LDR file and return 32x32 grid of colors."""
    grid = [[None for _ in range(32)] for _ in range(32)]
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('1 '):  # Part line
                parts = line.strip().split()
                color = int(parts[1])
                x = int(parts[2])
                z = int(parts[4])
                # Convert LDU to grid position (subtract 10 for center offset, divide by 20)
                gx = (x - 10) // 20
                gz = (z - 10) // 20
                if 0 <= gx < 32 and 0 <= gz < 32:
                    grid[gz][gx] = color
    return grid

def optimize_grid(grid):
    """Replace 1x1 tiles with larger tiles where possible."""
    placed = [[False for _ in range(32)] for _ in range(32)]
    pieces = []
    
    # Try to place larger pieces first
    for tile_w, tile_h, part in TILES:
        for y in range(32 - tile_h + 1):
            for x in range(32 - tile_w + 1):
                # Check if all cells in this area are same color and not placed
                color = grid[y][x]
                if color is None:
                    continue
                    
                can_place = True
                for dy in range(tile_h):
                    for dx in range(tile_w):
                        if placed[y + dy][x + dx] or grid[y + dy][x + dx] != color:
                            can_place = False
                            break
                    if not can_place:
                        break
                
                if can_place:
                    # Mark cells as placed
                    for dy in range(tile_h):
                        for dx in range(tile_w):
                            placed[y + dy][x + dx] = True
                    
                    # Calculate center position for LDraw
                    # For 1x1: center is at grid + 10
                    # For 2x2: center is at grid + 20 (between 4 studs)
                    # For 2x1: center x at grid + 20, z at grid + 10
                    cx = x * 20 + (tile_w * 10)
                    cz = y * 20 + (tile_h * 10)
                    
                    # Rotation matrix for 1x2 vs 2x1
                    if tile_w == 1 and tile_h == 2:
                        # Rotate 90 degrees
                        rot = "0 0 1 0 1 0 -1 0 0"
                    else:
                        rot = "1 0 0 0 1 0 0 0 1"
                    
                    pieces.append((color, cx, cz, rot, part, tile_w, tile_h))
    
    return pieces

def write_optimized_ldr(pieces, filename):
    """Write optimized LDR file."""
    with open(filename, 'w') as f:
        f.write("0 Coder Logo Mosaic 32x32 (Optimized)\n")
        f.write("0 Author: Mux\n")
        f.write("0 !LICENSE Redistributable under CCAL version 2.0\n")
        
        for color, x, z, rot, part, w, h in pieces:
            f.write(f"1 {color} {x} 0 {z} {rot} {part}.dat\n")
        
        f.write("0 STEP\n")
    
    # Count parts
    counts = {}
    for p in pieces:
        key = (p[4], p[5], p[6])  # part, w, h
        counts[key] = counts.get(key, 0) + 1
    
    return counts

if __name__ == "__main__":
    grid = parse_ldr("mosaic_32x32.ldr")
    pieces = optimize_grid(grid)
    counts = write_optimized_ldr(pieces, "mosaic_32x32_optimized.ldr")
    
    print("--- Optimized Parts List ---")
    total = 0
    for (part, w, h), count in sorted(counts.items()):
        print(f"{w}x{h} tile ({part}): {count}")
        total += count
    print(f"Total pieces: {total} (down from 1024)")
