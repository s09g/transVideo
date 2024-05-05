import logging

from utils import *




def merge_en_srt_by_time(video_id):
    logging.debug('merge_en_srt_by_time')
    file_dir = get_json_dir_prefix(video_id)
    srt_file_path = get_en_srt_path(video_id)

    gap = 2  # seconds
    merged_subtitles = []

    merge_map = []  # 记录合并前后的对应关系
    idx_to_time = {}
    timeline_to_en_srt = {}

    with open(srt_file_path, 'r', encoding='utf-8') as file:
        subtitle_blocks = file.read().strip().split('\n\n')

        # 用于临时存储待合并的字幕文本和时间
        temp_text = []
        temp_indexes = []  # 临时存储当前合并段落的原始索引

        start_time = None
        end_time = None

        for block in subtitle_blocks:
            lines = block.split('\n')
            if len(lines) < 3:
                raise ValueError("格式错误")
                continue
            index = int(lines[0])
            logging.debug("current index " + lines[0])
            idx_to_time[index] = lines[1]
            timeline_to_en_srt[lines[1]] = lines[2:]

            times = lines[1].split(' --> ')  # 解析时间码
            block_start = parse_time_to_sec(times[0])
            block_end = parse_time_to_sec(times[1])

            # 判断是否合并
            if start_time is None:
                # 初始化开始时间和结束时间
                start_time, end_time = block_start, block_end
                temp_text.append(' '.join(lines[2:]))
                temp_indexes.append(index)
            elif block_start - end_time <= gap:
                # 如果时间间隔小于等于gap秒，则合并
                temp_text.append(' '.join(lines[2:]))
                end_time = block_end  # 更新结束时间
                temp_indexes.append(index)
            else:
                # 如果时间间隔大于gap秒，先保存当前合并的字幕，再重新开始
                merged_subtitles.append(' '.join(temp_text))
                merge_map.append(temp_indexes)
                temp_text = [' '.join(lines[2:])]
                start_time, end_time = block_start, block_end
                temp_indexes = [index]

        # 确保最后一组字幕也被添加
        if temp_text:
            merged_subtitles.append(' '.join(temp_text))
            merge_map.append(temp_indexes)
    save_to_json(file_dir + 'idx_to_time.json', idx_to_time)
    save_to_json(file_dir + 'timeline_to_en_srt.json', timeline_to_en_srt)
    save_to_json(file_dir + 'merge_map.json', merge_map)
    save_to_json(file_dir + 'merged_subtitles.json', merged_subtitles)
