from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor, pipeline
from qwen_vl_utils import process_vision_info
import torch
import math
import time
import datetime
import os


#메모리 관리
'''
_total_mem = torch.cuda.get_device_properties(0).total_memory
_target_vram = 6 * 1024 ** 3  # 6 GiB
_fraction = _target_vram / _total_mem
torch.cuda.set_per_process_memory_fraction(_fraction, device=0)
max_memory = {"cuda:0": "6GiB"}
'''

#모델명
qwen_name = "unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit"
gemma_name = "unsloth/gemma-3-4b-pt-bnb-4bit"

from accelerate import init_empty_weights, load_checkpoint_and_dispatch

qwen_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=qwen_name,
        torch_dtype=torch.bfloat16  # 또는 "auto"
    )


gemma_model = pipeline(
    "text-generation",
    model=gemma_name,
    torch_dtype=torch.bfloat16  # 또는 "auto"
    )


qwen_processor = AutoProcessor.from_pretrained(qwen_name)
gemma_processor = AutoProcessor.from_pretrained(gemma_name)







path=r'./extracted_frames'

extracted_old_video = os.listdir(path)
extracted_video = []
for i in extracted_old_video:
    extracted_video.append(path+'/'+i)

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




# Preparation for inference
text = qwen_processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = qwen_processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
)
inputs = inputs.to("cuda")

# Inference
generated_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = qwen_processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)



end = time.time()


sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)



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
    },
    {
        "role": "assistant",
        "content": [
            {"type": "text", "text": result},
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Let's double-check. Is this a potentially dangerous situation?"},
        ],
    },

]
'''

role_assistant = {
        "role": "assistant",
        "content": [
            {"type": "text", "text": result},
        ]
    }
user_assistant= {
        "role": "user",
        "content": [
            {"type": "text", "text": "Let's double-check. Is this a potentially dangerous situation?"},
        ]
    }
messages.append(role_assistant)
messages.append(user_assistant)



text = qwen_processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = qwen_processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt",
)
inputs = inputs.to("cuda")

# Inference
generated_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = qwen_processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)



end = time.time()


sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)


role_assistant = {
        "role": "assistant",
        "content": [
            {"type": "text", "text": result},
        ]
    }
user_assistant= {
        "role": "user",
        "content": [
            {"type": "text", "text": "앞에 있는 대상에게 해당 내용에 대한 질문을 한국어로 말하세요."},
        ]
    }

messages.append(role_assistant)
messages.append(user_assistant)

output = gemma_model(text=messages, max_new_tokens=200)
print(output[0]["generated_text"][-1]["content"])
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)
