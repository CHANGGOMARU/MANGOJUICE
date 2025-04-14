from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import math
import time
import datetime


# default: Load the model on the available device(s)'''

model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Mungert/Qwen2.5-VL-3B-Instruct-GGUF/Qwen2.5-VL-3B-Instruct-q4_0.gguf", torch_dtype="auto", device_map="cpu")
#model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-2B", torch_dtype="auto", device_map="cuda")


# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
#     "unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit",
#     torch_dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

# default processer
processor = AutoProcessor.from_pretrained("unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit")






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
