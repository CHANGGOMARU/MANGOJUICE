from transformers import pipeline  
import torch
import os
import time
import datetime
from PIL import Image


pipe = pipeline(  
    "image-text-to-text",  
    model="unsloth/gemma-3-4b-it-bnb-4bit",
    torch_dtype="auto",
    device_map="auto",
    attn_implementation= "flash_attention_2",
    use_fast=True,
    load_in_4bit=True
)  

def resize_image(image_path):
    img = Image.open(image_path)

    target_width, target_height = 220, 220
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
  
output = pipe(text=messages, max_new_tokens=800)
end = time.time()

print(output[0]["generated_text"][-1]["content"])
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(str(result) + "초")


input_message = {"role": "assistant","content": [{"type": "text", "text": output}]}
messages.append(input_message)

input_message = {"role": "user","content": [{"type": "text", "text": "Let's double-check. Is this a potentially dangerous situation?"}]}
messages.append(input_message)

print(messages)

output = pipe(text=messages, max_new_tokens=800)
end = time.time()

print(output[0]["generated_text"][-1]["content"])
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(str(result) + "초")
