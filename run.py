from download_video import *
from merge_caption import *
from split_caption_auto import *
from split_caption_manual import *
from handle_zh_srt import *
from translate import *
from embed_srt import *
from logger import setup_logging


video_id = 'zduSFxRajkE'
setup_logging(video_id)
logging.debug('video id : ' + video_id)
video_path = download_video(video_id)
download_caption(video_id)
merge_en_srt_by_time(video_id)
split_auto(video_id)
# split_video_manual(video_id)
time_to_zh_srt(video_id)
translate(video_id)
embed_zh_srt("video/zduSFxRajkE/1.mp4", video_id)



