from fastapi import FastAPI
from google.adk.runners import InMemoryRunner

from agentBlogger import (
    create_research_agent, 
    create_summarizer_agent, 
    create_root_agent
)

# 1. 서버 시작 시 에이전트와 러너를 한 번만 생성
print("🚀 API Server starting ...")
research_agent = create_research_agent()
summarizer_agent = create_summarizer_agent()
root_agent = create_root_agent(research_agent, summarizer_agent)

# 2. 아래 runner 객체를 모든 api 요청에서 재사용
runner = InMemoryRunner(agent=root_agent)
print("✅ Runner is ready.")

# 3. FastAPI 앱 생성
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World! This is the Blog Post Generator API."}

@app.get("/generate-blog-post")
async def generate_blog_post_endpoint(topic: str):
    print(f"🔥 '{topic}' Blog post generation request received")

    # 이미 만들어진 runner를 사용해 요청 처리
    response = await runner.run_debug(topic)
    return {"blog_post": response}