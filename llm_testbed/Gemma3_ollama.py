from ollama import chat
from ollama import ChatResponse
import os
import time
import datetime
from PIL import Image



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


class split(object):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "'"+self.name+"'"



path=r'./extracted_frames'

extracted_old_video = os.listdir(path)
extracted_video = []
for i in extracted_old_video:
    extracted_video.append(path+'/'+i)



start = time.time()


messages_list = [   
    {
        "role": "system",  
        "content": "Keep all answers as short, simple, and accurate as possible.",
        "role": "user",  
        "content": "Is the person in the video falling or in a dangerous situation? Treat falls on fluffy objects, such as mats, as dangerous.",
        
        
}
]
a = 1

for frame in extracted_video:
     messages_list[0][split("content")] = str(a)+" frame"
     a =+ 1
     messages_list[0][split("images")] = resize_image(frame)


print(messages_list)

response: ChatResponse = chat(model='gemma3:4b-it-qat', messages=messages_list)
  
end = time.time()

print(response.message.content)
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(str(result) + "초")



messages_list[0][split("role")] = "assistant"
messages_list[0][split("content")] = response.message.content


messages_list[0][split("role")] = "user"
messages_list[0][split("content")] = "Let's double-check. Is this a potentially dangerous situation?"

#print(messages)

response: ChatResponse = chat(model='gemma3:4b-it-qat', messages=messages_list)
end = time.time()

print(response.message.content)
sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(str(result) + "초")
