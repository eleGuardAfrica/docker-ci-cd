from fastapi import FastAPI
from pydantic import BaseModel
from ayrshare import SocialPost

social = SocialPost("3F73D951-0CF94226-B0C5D651-2ABAB5F3")

app = FastAPI()

class ShareRequest(BaseModel):
    post: str
    platforms: list


def post_now(post: str, platforms: list):
    json_data = {
        "post": post,
        "platforms": platforms
    }
    response = social.post(json_data)
    return response  # IMPORTANT: return this


@app.get("/")
def hello():
    return {"message": "Hello, Allord!"}


@app.post("/share")
def share_post(req: ShareRequest):
    response = post_now(req.post, req.platforms)
    return {"post_status": response}
