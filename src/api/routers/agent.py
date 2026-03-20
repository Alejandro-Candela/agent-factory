"""Agent router — handles chat and agent interactions."""
from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(message: str) -> dict:
    """Process a chat message through the agent pipeline. TODO: Implement."""
    return {"message": f"Echo: {message}", "thread_id": "placeholder", "sources": []}
