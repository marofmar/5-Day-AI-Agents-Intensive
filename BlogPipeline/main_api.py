from fastapi import FastAPI
from agentBlogger import main as generate_blog_post

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/generate-blog-post")
async def generate_blog_post_endpoint(topic: str):
    response = await generate_blog_post(topic)
    return {"blog_post": response}