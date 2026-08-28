#!/usr/bin/env python3
"""Generate a GIF of a spinning cube with 28 frames."""

import numpy as np
from PIL import Image, ImageDraw

def create_cube_frame(frame_num, total_frames, size=50):
    """Create a single frame of the spinning cube."""
    # Calculate rotation angle for this frame (full 360° rotation)
    angle = 2 * np.pi * frame_num / total_frames
    
    # Cube vertices (centered at origin)
    cube_size = 15
    vertices = np.array([
        [-cube_size, -cube_size, -cube_size],
        [cube_size, -cube_size, -cube_size],
        [cube_size, cube_size, -cube_size],
        [-cube_size, cube_size, -cube_size],
        [-cube_size, -cube_size, cube_size],
        [cube_size, -cube_size, cube_size],
        [cube_size, cube_size, cube_size],
        [-cube_size, cube_size, cube_size],
    ])
    
    # Rotation matrix around Y axis
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    rotation_y = np.array([
        [cos_a, 0, sin_a],
        [0, 1, 0],
        [-sin_a, 0, cos_a]
    ])
    
    # Rotate vertices
    rotated = vertices @ rotation_y.T
    
    # Simple perspective projection
    distance = 60
    projected = []
    for v in rotated:
        z = v[2] + distance
        x = v[0] * distance / z
        y = v[1] * distance / z
        projected.append((x + size//2, y + size//2))
    
    # Define edges (pairs of vertex indices)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw edges only (no faces)
    for edge in edges:
        p1 = projected[edge[0]]
        p2 = projected[edge[1]]
        draw.line([p1, p2], fill=(0, 0, 0, 255), width=4)
    
    return img

def main():
    total_frames = 28
    frames = []
    
    print(f"Generating {total_frames} frames...")
    for i in range(total_frames):
        frame = create_cube_frame(i, total_frames)
        frames.append(frame)
        print(f"  Frame {i+1}/{total_frames}")
    
    # Save as GIF with transparency
    output_path = '/workspace/spinning_cube.gif'
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 100ms per frame = 10 FPS
        loop=0,  # Loop forever
        transparency=0,
        disposal=2
    )
    
    print(f"\nGIF saved to: {output_path}")
    print(f"Total frames: {total_frames}")
    print(f"Rotation: 360° over {total_frames} frames ({360/total_frames:.2f}° per frame)")

if __name__ == '__main__':
    main()
