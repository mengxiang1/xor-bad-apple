import os
import numpy as np
from PIL import Image
import subprocess

height = width = None
cum_frames = None
video_frames = []

for i, filename in enumerate(os.listdir("./frames"), start=1):
    image_path = f"./frames/frame_{i}.png"
    with Image.open(image_path) as image:
        image = image.convert('L')
        binary_data = np.array(image)
        if height is None:
            height, width = binary_data.shape
        if cum_frames is None:
            frame = np.zeros((height, width), dtype=np.uint8)
        else:
            binary_data = np.bitwise_xor(binary_data, cum_frames)
            frame = binary_data
        cum_frames = binary_data
        video_frames.append(frame)
    if i == 100: break

ffmpeg = subprocess.Popen([
    "ffmpeg",
    "-y",
    "-framerate", "30",
    "-f", "rawvideo",
    "-pixel_format", "gray",
    "-video_size", f"{width}x{height}",
    "-i", "-",
    "-i", "video.mp4",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    "-shortest",
    "output.mp4"
], stdin=subprocess.PIPE)

for frame in video_frames:
    ffmpeg.stdin.write(frame.tobytes())

ffmpeg.stdin.close()
ffmpeg.wait()
