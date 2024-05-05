from utils import *

def time_to_zh_srt(video_id):
    zh_srt_file_path = get_zh_srt_path(video_id)
    time_to_en_text = read_from_json(get_json_dir_prefix(video_id) + 'timeline_to_en_srt.json')
    timeline_to_srt = {}

    parsed_entries = parse_srt_content_to_dict(zh_srt_file_path)
    for timeline in time_to_en_text.keys():
        if timeline in parsed_entries:
            timeline_to_srt[timeline] = parsed_entries[timeline]
        else:
            timeline_to_srt[timeline] = [""]

    save_to_json(get_json_dir_prefix(video_id) + 'timeline_to_zh_srt.json', timeline_to_srt)