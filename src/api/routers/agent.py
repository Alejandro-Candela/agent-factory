"""Agent router — handles chat and agent interactions."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest) -> dict:
    """Process a chat message through the agent pipeline. TODO: Implement."""
    return {"message": f"Echo: {request.message}", "thread_id": "placeholder", "sources": []}
