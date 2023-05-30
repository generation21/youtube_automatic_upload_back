from dotenv import load_dotenv
from os import environ

# load .env
load_dotenv()

OPENAI_KEY = environ.get('OPENAI_KEY')

HUGGINGFACE_MODEL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HUGGINGFACE_KEY =  environ.get('HUGGINGFACE_KEY')