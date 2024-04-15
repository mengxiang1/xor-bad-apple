import subprocess
import os

video_file = 'video.mp4'
output_dir = 'frames'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

command = ['ffmpeg', '-i', video_file, '-vf', 'fps=30', f'{output_dir}/frame_%d.png']
subprocess.call(command)
