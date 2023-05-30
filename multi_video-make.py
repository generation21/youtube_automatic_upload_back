from PIL import Image, ImageDraw, ImageFont
from textwrap import fill
import requests
import io
from gtts import gTTS
from moviepy.editor import *
import torch
import random
import numpy as np 

output = './outputs'

# ========= 이미지 로드 ============
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.status_code)
    return response.content

clips = []

## backgroud music
music_name = random.choice(os.listdir("./music"))
background_audio  = AudioFileClip(f'./music/{music_name}')
    
quotes = ["I think the best work comes from when you've prepared as much as you can and you really let go.",
"When suddenly you go to college, and you have this independence, there are so many things that you could get out of balance.",
"There's something about acting that's mysterious. You can prepare all you want, but the moment calls for something else.",
"Anytime I'm acting, I'm playing a character. It's just the work. It's me lending myself to a part.",
"I just try to think about how I can grow, really be honest with myself, listen to people close to me who care about me who are honest with me.",
]
start_time = 0
end_time = -1
for i, quote in enumerate(quotes):
    try_nums = 5
    for try_num in range(try_nums):
        try:
            image_bytes = query({
                "inputs": f"Draw a nice landscape to match the quote {quote}, masterpiece, high quality, relaxing,  random seed {random.randint(0,2**62-1)}, No text should be included in the picture.", #"Paint me a proper picture of Mahershala Ali', ",
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



    # 텍스트 음성 변환
    tts = gTTS(text=quote, lang='en')
    tts.save(f'{output}/example_text_{i}.mp3')
    # Load audio
    audio_clip = AudioFileClip(f'{output}/example_text_{i}.mp3')
    
    
    # 배경 오디오와 교차
    end_time = audio_clip.duration + start_time
    temp_bg_audio = background_audio.subclip(start_time, end_time)
    start_time = end_time
     # 배경 오디오의 볼륨을 줄인 뒤 음성 클립과 함께 애니메이션 클립의 오디오를 결합
    # combined_audio =  (audio_clip.volumex(0.6) + temp_bg_audio.volumex(0.4)).set_duration(audio_clip.duration)
    final_clip = CompositeAudioClip([audio_clip.volumex(1.2), temp_bg_audio.volumex(0.5)])
    
    # Load image (display for 10 seconds)
    img_clip = ImageClip(f'{output}/example_image_with_text_{i}.png', duration=final_clip.duration)

    # Set the frames per second
    img_clip.fps = 24

    # Add the audio clip to the image clip
    img_clip = img_clip.set_audio(final_clip)
    clips.append(img_clip)

# Concatenate all the clips
final_clip = concatenate_videoclips(clips)

# Save as video
final_clip.write_videofile(f'{output}/final_video.mp4', codec='mpeg4', audio_codec='aac', bitrate='4000k')
