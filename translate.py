from utils import *
from openai_util import *

def rebuild(zh_srt_result, idx_to_time):
    # 当前处理的段落号
    curt_idx = None
    # 当前段落的文本列表
    current_text = []
    polish_zh_text_list = []

    # 按行遍历文本
    for line in zh_srt_result.strip().split('\n'):
        # 检查是否是段落号（仅包含数字）
        if line.isdigit():
            # 如果之前已经有段落在处理中，则保存该段落
            if curt_idx is not None:
                text = ' '.join(current_text).strip()
                polish_zh_text_list.append(f"{curt_idx}\n{idx_to_time[str(curt_idx)]}\n{text}")
                current_text = []
            curt_idx = int(line)
        else:
            # 添加文本到当前段落
            current_text.append(line)

    # 保存最后一个段落
    if curt_idx is not None and current_text:
        text = ' '.join(current_text).strip()
        polish_zh_text_list.append(f"{curt_idx}\n{idx_to_time[str(curt_idx)]}\n{text}")

    return "\n\n".join(polish_zh_text_list)

def get_paragraph(paragraph_idx_list, idx_to_time, timeline_to_srt):
    line_srt_list = []
    for idx in paragraph_idx_list:
        timeline = idx_to_time[str(idx)]
        line_srt_txt = "\n".join(timeline_to_srt[timeline])
        line_srt_list.append(f"{idx}\n{line_srt_txt}")
    paragraph_srt = "\n\n".join(line_srt_list)
    srt_dict = {idx: text for idx, text in zip(paragraph_idx_list, paragraph_srt)}
    return paragraph_srt, srt_dict

def get_range_srt(start, end, srt_dict):
    srt_seg = [srt_dict[idx] for idx in range(start, end + 1)]
    return "\n\n".join(srt_seg)

def translate(video_id):
    merge_map = read_from_json(get_json_dir_prefix(video_id) + 'merge_map.json')
    idx_to_time = read_from_json(get_json_dir_prefix(video_id) + 'idx_to_time.json')
    timeline_to_en_srt = read_from_json(get_json_dir_prefix(video_id) + 'timeline_to_en_srt.json')
    timeline_to_zh_srt = read_from_json(get_json_dir_prefix(video_id) + 'timeline_to_zh_srt.json')

    for paragraph_idx_list in merge_map:
        en_srt, en_srt_dict = get_paragraph(paragraph_idx_list, idx_to_time, timeline_to_en_srt)
        zh_srt, zh_srt_dict = get_paragraph(paragraph_idx_list, idx_to_time, timeline_to_zh_srt)

        logic_idx_list = get_logic_segment(en_srt)
        append_to_file(get_json_dir_prefix(video_id) + "cached_logic_segments.json",  logic_idx_list["segments"] + ",")
        for segment in logic_idx_list["segments"]:
            start, end = segment
            zh_seg_srt = get_range_srt(start, end, zh_srt_dict)
            en_seg_srt = get_range_srt(start, end, en_srt_dict)

            zh_srt_result = gpt_polish(en_seg_srt, zh_seg_srt)
            polish_zh_text = rebuild(zh_srt_result, idx_to_time)
            append_to_file(get_output_zh_srt(video_id), polish_zh_text + "\n\n")
