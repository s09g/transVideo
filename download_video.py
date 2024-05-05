from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from utils import *
import logging

def download_video(video_id):
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    logging.debug(video_url)
    yt = YouTube(video_url)
    output_path = get_video_dir(video_id)
    output_name = yt.streams.get_highest_resolution().download(output_path=output_path)
    logging.debug(f'video文件已保存至 {output_name}')
    return output_name

def download_caption(video_id):
    try:
        en_srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        formatter = SRTFormatter()
        en_srt_path = get_en_srt_path(video_id)
        with open(en_srt_path, 'w', encoding='utf-8') as file:
            srt_content = formatter.format_transcript(en_srt)
            file.write(srt_content)
        logging.debug(f'英文字幕文件已保存至 {en_srt_path}')
    except Exception as e:
        logging.error(f"获取英文字幕失败: {e}")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        translated_transcript = transcript.translate('zh-Hans')
        zh_srt = translated_transcript.fetch()
        zh_srt_path = get_zh_srt_path(video_id)
        with open(zh_srt_path, 'w', encoding='utf-8') as file:
            srt_content = formatter.format_transcript(zh_srt)
            file.write(srt_content)
        logging.debug(f'中文字幕文件已保存至 {zh_srt_path}')
    except Exception as e:
        logging.error(f"获取中文字幕失败: {e}")

