#from unsloth import FastLanguageModel
from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import math
import time
import datetime



#메모리 3GB로 제한
import torch
_total_mem = torch.cuda.get_device_properties(0).total_memory
_target_vram = 4 * 1024 ** 3  # 2 GiB
_fraction = _target_vram / _total_mem
torch.cuda.set_per_process_memory_fraction(_fraction, device=0)
max_memory = {"cuda:0": "4GiB"}



#리눅스 계열에서만 지원하는 코드. 작동확인 필요.
'''
import resource
_soft, _hard = _target_vram, _target_vram
resource.setrlimit(resource.RLIMIT_AS, (_soft, _hard))
'''

#unsloth로 양자화한 모델이르모, unsloth 모델을 로딩함.
#from unsloth import FastLanguageModel
#max_memory = {"cuda:0": "8GiB"}

model_name = "unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit"

#accelerate 모델로 12GB 가량의 큰 모델을 사용전 메모리를 효율적으로 분할하게 함.
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

# default: Load the model on the available device(s)'''
'''with init_empty_weights():
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=model_name,
        torch_dtype="auto"  # 또는 "auto"
    )
'''
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=model_name,
        torch_dtype="auto"  # 또는 "auto"
    )


"""
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        pretrained_model_name_or_path=model_name,
        torch_dtype="auto",  # 또는 "auto"
        attn_implementation="flash_attention_2"
    )

"""


'''
with init_empty_weights():
    model = FastLanguageModel.from_pretrained("unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit", torch_dtype="auto", device_map="auto",max_memory = max_memory,load_in_4bit = True)
'''


'''
model = load_checkpoint_and_dispatch(
    model,
    model_name,
    device_map="auto",
    no_split_module_classes=["Qwen2_5_VLForConditionalGeneration"]
)
'''
#model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-2B", torch_dtype="auto", device_map="cuda")


# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
#     "unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit",
#     torch_dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

# default processer
processor = AutoProcessor.from_pretrained(model_name)






start = time.time()
'''
# Messages containing a video url and a text query
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "video",
                "video": "00151_H_A_BY_C1.mp4",
            },
            {"type": "text", "text": "Describe this video."},
        ],
    }
]
'''
import os
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
text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = processor(
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
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)



end = time.time()


sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)




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




text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
image_inputs, video_inputs = process_vision_info(messages)
inputs = processor(
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
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)



end = time.time()


sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)
