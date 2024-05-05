import logging
from utils import *

def merge_srt_by_time(video_id, src_file_path, file_dir):
    gap = 2
    merged_subtitles = []
    merged_map = []

    srt_content_list = parse_srt_content_to_list(src_file_path, file_dir)

    # 临时存储
    temp_text = []
    temp_indexes = []
    start_time = None
    end_time = None
    for entry in srt_content_list:
        index = entry["index"]

        times = entry["time"].split(' --> ')  # 解析时间码
        block_start = parse_time_to_sec(times[0])
        block_end = parse_time_to_sec(times[1])

        # 判断是否合并
        if start_time is None:
            # 初始化开始时间和结束时间
            start_time, end_time = block_start, block_end
            temp_text.append(' '.join(entry["text"]))
            temp_indexes.append(index)
        elif block_start - end_time <= gap:
            # 如果时间间隔小于等于gap秒，则合并
            temp_text.append(' '.join(entry["text"]))
            end_time = block_end  # 更新结束时间
            temp_indexes.append(index)
        else:
            # 如果时间间隔大于gap秒，先保存当前合并的字幕，再重新开始
            merged_subtitles.append(' '.join(temp_text))
            merged_map.append(temp_indexes)
            temp_text = [' '.join(entry["text"])]
            start_time, end_time = block_start, block_end
            temp_indexes = [index]

    if temp_text:
        merged_subtitles.append(' '.join(temp_text))
        merged_map.append(temp_indexes)

    save_to_json(file_dir + 'merge_map.json', merged_map)
    save_to_json(file_dir + 'merged_subtitles.json', merged_subtitles)
    save_to_json(file_dir + 'merged_subtitles_canary.json',
                 build_merged_subtitles(merged_map,
                                        build_idx_text_mapping(srt_content_list)))

    save_to_json(file_dir + 'idx_to_time.json', build_idx_time_mapping(srt_content_list))
    save_to_json(file_dir + 'timeline_to_en_srt.json', build_time_srt_text_mapping(srt_content_list))

def split_auto(video_id):
    logging.debug('split_auto')

    merge_srt_by_time(video_id,
                      src_file_path=get_en_srt_path(video_id),
                      file_dir=get_json_dir_prefix(video_id))

