from PIL import Image, ImageDraw, ImageFont
from textwrap import fill
import requests
import io
from gtts import gTTS
from moviepy.editor import *
import torch
import random
import numpy as np 

from libs.config import HUGGINGFACE_MODEL, HUGGINGFACE_KEY
output = './outputs'

# ========= 이미지 로드 ============



def query(payload, huggingface_key):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_KEY}"}
    response = requests.post(HUGGINGFACE_MODEL, headers=headers, json=payload)

    return response.content

def image_generation(huggingface_key="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", texts=""):
    
    clips = []

    

    for i, text in enumerate(texts):
        try_nums = 5
        for try_num in range(try_nums):
            try:
                image_bytes = query({
                    "inputs": f"Draw a nice landscape to match the {text}, masterpiece, high quality, relaxing,  random seed {random.randint(0,2**62-1)}, No text should be included in the picture.", #"Paint me a proper picture of Mahershala Ali', ",
                    "parameters": {"num_inference_steps": 50,
                                "guidance_scale": 7.5, 
                                "negative_prompt": "low quality, nsfw, phrase",
                                "num_images_per_prompt": 1,
                        
                                }
                    })
                img = Image.open(io.BytesIO(image_bytes))
                break
            except:
                Exception (f"try {try_num}")

    
    image_arr = np.asarray(img)
    # 이미지의 새로운 높이를 계산합니다. (pad_size만큼 확장)
    original_height, original_width = image_arr.shape[:2]
    pad_size = 250
    new_height = original_height + pad_size*2 

    # 아래 위로 검정색(padding)을 더합니다.
    padded_image_arr = np.pad(image_arr, ((pad_size, pad_size), (0, 0), (0, 0)), mode='constant', constant_values=(0,0))
    img = Image.fromarray(padded_image_arr).resize((1080, 1920)) #(width, height).
    
    draw = ImageDraw.Draw(img)

    # 텍스트 및 폰트 설정

    wrapped_text = fill(quote, width=30)
    lines = wrapped_text.split('\n')  # 줄 바꿈 위치를 기반으로 라인 리스트 생성
    font_size = 60

    font = ImageFont.truetype('./font/NanumJangMiCe.ttf', font_size)
    
    # font.set_variation_by_name('Italic') #['Normal', 'Bold', 'Italic', 'Bold, Italic']

    # 텍스트 그리기
    img_w, img_h = img.size
    y_position = (img_h - font_size * ( len(lines) - 15 )) // 2
    for line in lines:
        text_w, text_h = draw.textsize(line, font=font)
        x_position = (img_w - text_w) // 2  # 이미지 가운데 정렬
        draw.text((x_position, y_position), line, (237, 230, 211), font=font, stroke_width=1, stroke_fill=(0,0,0))
        y_position += font_size
    
    descript_font_size = 30
    descript = "only uses ai generation"
    font = ImageFont.truetype('./font/NanumJangMiCe.ttf', descript_font_size)
    text_w, text_h = draw.textsize(descript, font=font)
    draw.text((img_w-text_w, img_h-descript_font_size), descript, (237, 230, 211), font=font, stroke_width=1, stroke_fill=(0,0,0))
    # 이미지 저장
    img.save(f'{output}/example_image_with_text_{i}.png')

