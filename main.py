from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.agent import TutorAgent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# اجازه اتصال از UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# یه agent برای هر session
agent = TutorAgent()

class ChatRequest(BaseModel):
    message: str
    level: str = "beginner"

class LevelRequest(BaseModel):
    level: str

@app.post("/chat")
async def chat(request: ChatRequest):
    agent.set_level(request.level)
    response = agent.chat(request.message)
    return {"response": response}

@app.post("/set-level")
async def set_level(request: LevelRequest):
    result = agent.set_level(request.level)
    return {"result": result}

@app.get("/context")
async def get_context():
    return {"context": agent.memory.get_context_summary()}

@app.get("/")
async def root():
    return {"status": "AI Tutor is running!"}