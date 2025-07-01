from transformers import AutoProcessor, Gemma3ForConditionalGeneration
import torch
import os
import time
import datetime
from PIL import Image


model = Gemma3ForConditionalGeneration.from_pretrained(
    "google/gemma-3-4b-it-qat-q4_0-gguf",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="sdpa"
) 


processor = AutoProcessor.from_pretrained(
    "google/gemma-3-4b-it-qat-q4_0-gguf",
    padding_side="left"
)

def resize_image(image_path):
    img = Image.open(image_path)

    target_width, target_height = 360, 420
    # Calculate the target size (maximum width and height).
    if target_width and target_height:
        max_size = (target_width, target_height)
    elif target_width:
        max_size = (target_width, img.height)
    elif target_height:
        max_size = (img.width, target_height)

    img.thumbnail(max_size)

    return img



path=r'./extracted_frames'

extracted_old_video = os.listdir(path)
extracted_video = []
for i in extracted_old_video:
    extracted_video.append(path+'/'+i)



start = time.time()
messages = [   
    {  
        "role": "user",  
        "content": [
            {"type": "text", "text": "Is the person in the video falling or in a dangerous situation? Treat falls on fluffy objects, such as mats, as dangerous."}  
        ]  
    }  
]
a = 1
for frame in extracted_video:
     messages[0]["content"].append({"type": "text", "text": str(a)+" frame"})
     a =+ 1
     messages[0]["content"].append({"type": "image", "image": resize_image(frame)})


print(messages)
  
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    add_generation_prompt=True,
).to("cuda")
output = model.generate(**inputs, max_new_tokens=800, cache_implementation="static")
end = time.time()

print(processor.decode(output[0], skip_special_tokens=True))
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(str(result) + "초")
