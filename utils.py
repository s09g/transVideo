import re, json, logging
from datetime import datetime, timedelta

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

def read_from_json(filename):
    with open(filename, 'r') as json_file:
        data_loaded = json.load(json_file)
    return data_loaded

def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(str(text))

def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read()
    return lines

def get_en_srt_path(video_id):
    return f"video/{video_id}/{video_id}-en.srt"

def get_zh_srt_path(video_id):
    return f"video/{video_id}/{video_id}-zh.srt"

def get_video_dir(video_id):
    return f"video/{video_id}"

def get_json_dir_prefix(video_id):
    return f"video/{video_id}/"

def read_srt_file_by_line(filename):
    """读取SRT文件内容并返回行列表。"""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def get_output_zh_srt(video_id):
    return f"video/{video_id}/final.srt"

def parse_srt_content_to_list(src_file_path):
    logging.debug('parse_srt_content_to_list')
    srt_content = read_from_file(src_file_path)

    # 将文件分割成字幕块
    blocks = re.split(r'\n\n', srt_content)
    subtitles = []

    for block in blocks:
        # 分割每个字幕块为行
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            subtitle = {
                'index': lines[0],
                'time': lines[1],
                'text': ' '.join(lines[2:])
            }
            subtitles.append(subtitle)
    return subtitles

def build_idx_time_mapping(srt_content_list):
    idx_to_time = {entry["index"]: entry["time"] for entry in srt_content_list}
    return idx_to_time

def build_time_srt_text_mapping(srt_content_list):
    timeline_to_srt_text = {entry["time"]: entry["text"] for entry in srt_content_list}
    return timeline_to_srt_text

def build_idx_text_mapping(srt_content_list):
    idx_to_srt_text = {entry["index"]: entry["text"] for entry in srt_content_list}
    return idx_to_srt_text
def build_merged_subtitles(merged_map, idx_to_srt):
    merged_subtitles = []
    for seg in merged_map:
        temp_text = [idx_to_srt[id] for id in seg]
        merged_subtitles.append(' '.join(temp_text))
    return merged_subtitles


def parse_srt_content_to_dict(srt_file_path):
    logging.debug("解析SRT文件内容，提取时间轴和文本信息。")
    l = parse_srt_content_to_list(srt_file_path)
    res = {e["time"]: e["text"] for e in l}
    return res

def parse_time_to_sec(srt_time):
    """将SRT时间格式转换为秒"""
    # 正确的分割正则表达式，仅匹配冒号和逗号
    parts = re.split('[:,]', srt_time)
    if len(parts) == 4:
        hours, minutes, seconds, milliseconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    else:
        raise ValueError("时间格式错误")

def parse_time_to_datetime(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')