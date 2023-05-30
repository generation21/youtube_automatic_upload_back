import os

from fastapi import APIRouter
from pydantic import BaseModel
import openai
import re

from .image_generation import image_generation
from libs.config import OPENAI_KEY
router = APIRouter(
    prefix="/generation",
)

class Item(BaseModel):
    huggingface_key: str
    description: str | None = None
    price: float
    tax: float | None = None

@router.post("/{generation_type}")
async def read_item(generation_type: str, item: Item):
    if generation_type == 'famous_quotes':
         message = "Pick out 5 famous quotes"
    elif generation_type == 'ai_generation':
        message = 'Make 5 phrases that heal you yourself'
    
    openai.api_key = OPENAI_KEY 
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=256,
        temperature=2
    )

    text = completion.choices[0].text
    text = [re.sub(r'^[\d.]*\s*', '', line.strip()) for line in text.splitlines() if line.strip()]

    image_generation(huggingface_key = item.huggingface_key)

    return text