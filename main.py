
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from domain.video_generation import generation_router
origins = [
    "http://127.0.0.1:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation_router.router)


