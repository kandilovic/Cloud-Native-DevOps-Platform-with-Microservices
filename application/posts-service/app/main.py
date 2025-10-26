from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Posts Service")

REDIS_HOST = os.getenv("REDIS_HOST")
use_redis = False
redis_client = None

if REDIS_HOST:
    try:
        import redis
        redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
        redis_client.ping()
        use_redis = True
    except Exception:
        use_redis = False

_posts = []
_id = 1

class PostIn(BaseModel):
    title: str
    body: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "posts", "redis_connected": use_redis}

@app.post("/posts")
def create_post(p: PostIn):
    global _id
    post = {"id": _id, "title": p.title, "body": p.body}
    _id += 1
    if use_redis:
        redis_client.rpush("posts", str(post))
    else:
        _posts.append(post)
    return post

@app.get("/posts")
def list_posts():
    if use_redis:
        items = redis_client.lrange("posts", 0, -1)
        return {"posts": [eval(item) for item in items]}
    return {"posts": _posts}