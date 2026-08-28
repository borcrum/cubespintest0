#!/usr/bin/env python3
"""Generate a GIF of a spinning cube with 28 frames."""

import numpy as np
from PIL import Image, ImageDraw

def create_cube_frame(frame_num, total_frames, size=400):
    """Create a single frame of the spinning cube."""
    # Calculate rotation angle for this frame (full 360° rotation)
    angle = 2 * np.pi * frame_num / total_frames
    
    # Cube vertices (centered at origin)
    cube_size = 100
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
    distance = 400
    projected = []
    for v in rotated:
        z = v[2] + distance
        x = v[0] * distance / z
        y = v[1] * distance / z
        projected.append((x + size//2, y + size//2))
    
    # Define faces (indices of vertices)
    faces = [
        (0, 1, 2, 3),  # Back
        (4, 5, 6, 7),  # Front
        (0, 1, 5, 4),  # Bottom
        (2, 3, 7, 6),  # Top
        (0, 3, 7, 4),  # Left
        (1, 2, 6, 5),  # Right
    ]
    
    # Face colors (different shades for visibility)
    face_colors = [
        '#4a4a4a',  # Back - dark gray
        '#6a6a6a',  # Front - medium gray
        '#5a5a5a',  # Bottom
        '#7a7a7a',  # Top - light gray
        '#505050',  # Left
        '#606060',  # Right
    ]
    
    # Create image
    img = Image.new('RGB', (size, size), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Calculate face depths for simple Z-sorting
    face_depths = []
    for i, face in enumerate(faces):
        avg_z = sum(rotated[v][2] for v in face) / 4
        face_depths.append((avg_z, i))
    
    # Sort faces by depth (draw back faces first)
    face_depths.sort()
    
    # Draw faces from back to front
    for _, face_idx in face_depths:
        face = faces[face_idx]
        points = [projected[v] for v in face]
        draw.polygon(points, fill=face_colors[face_idx], outline='#000000')
    
    return img

def main():
    total_frames = 28
    frames = []
    
    print(f"Generating {total_frames} frames...")
    for i in range(total_frames):
        frame = create_cube_frame(i, total_frames)
        frames.append(frame)
        print(f"  Frame {i+1}/{total_frames}")
    
    # Save as GIF
    output_path = '/workspace/spinning_cube.gif'
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 100ms per frame = 10 FPS
        loop=0,  # Loop forever
        disposal=2
    )
    
    print(f"\nGIF saved to: {output_path}")
    print(f"Total frames: {total_frames}")
    print(f"Rotation: 360° over {total_frames} frames ({360/total_frames:.2f}° per frame)")

if __name__ == '__main__':
    main()
