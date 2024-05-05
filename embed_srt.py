import subprocess
from utils import *
def embed_zh_srt(video_path, video_id):
    """
#!/usr/bin/env bash
ffmpeg -i ./video/1.mp4 -vf subtitles=final_zh.srt ./video/output.mp4

    """
    logging.debug("embed_zh_srt...")
    command = f"ffmpeg -i {video_path} -vf subtitles={get_output_zh_srt(video_id)} {get_video_dir(video_id)}/output.mp4"
    logging.debug(command)
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)