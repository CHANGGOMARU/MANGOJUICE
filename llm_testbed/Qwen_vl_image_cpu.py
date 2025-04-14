from llama_cpp import Llama
import math
import time
import datetime



llm = Llama.from_pretrained(
	repo_id="Mungert/Qwen2.5-VL-3B-Instruct-GGUF",
	filename="Qwen2.5-VL-3B-Instruct-q4_0.gguf",
)


import os
path=r'./extracted_frames'

extracted_old_video = os.listdir(path)
extracted_video = []
for i in extracted_old_video:
    extracted_video.append(path+'/'+i)

   
'''
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "video",
                "video": extracted_video,
                "max_pixels": 360 * 420,
            },
            {"type": "text", "text": "Describe this video. Is the person in the video falling or in a dangerous situation? Treat falls on fluffy objects, such as mats, as dangerous."},
        ],
    }
]


'''
llm.create_chat_completion(
	messages = [
            {
        "role": "user",
        "content": [
            {
                "type": "video",
                "video": extracted_video,
                "max_pixels": 360 * 420,
            },
            {"type": "text", "text": "Describe this video. Is the person in the video falling or in a dangerous situation? Treat falls on fluffy objects, such as mats, as dangerous."},
        ],
    }
]
)
