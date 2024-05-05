import os
import json
from logger import logging
from openai import OpenAI
import logging

client = OpenAI()


def get_logic_segment(en_srt):
    with open('./prompt/get_logic_segment.txt', 'r') as file:
        get_logic_segment_prompt_text = file.read()

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={ "type": "json_object" },
        temperature=0,
        messages=[
            {"role": "system", "content": get_logic_segment_prompt_text},
            {"role": "user", "content": en_srt}
        ]
    )
    res = response.choices[0].message.content
    logging.debug(res)
    return json.loads(res)


def gpt_polish(en_seg_srt, zh_seg_srt):
    # return ""
    with open('./prompt/gpt_polish.txt', 'r') as file:
        gpt_polish_prompt_text = file.read()

    response = client.chat.completions.create(
        model="gpt-4",
        # response_format={ "type": "json_object" },
        temperature=0,
        messages=[
            {"role": "system", "content": gpt_polish_prompt_text},
            {"role": "user", "content": f"##英文字幕##\n```{en_seg_srt}```\n##中文字幕##\n```{zh_seg_srt}```\n"}
        ]
    )
    ans = response.choices[0].message.content[12:-3]
    logging.debug(ans)
    return ans