"""Conversation Service - Database operations for Conversations"""

from datetime import datetime, timezone
from typing import Optional, List
from database import conversations_collection
from models import Conversation


def create_conversation(session_id: str, role: str, content: str, agent_type: Optional[str] = None) -> Conversation:
    """Create a new conversation message"""
    now = datetime.now(timezone.utc)
    doc = {
        "session_id": session_id,
        "message": {"role": role, "content": content, "timestamp": now},
        "created_at": now,
        "agent_type": agent_type
    }
    result = conversations_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc  # type: ignore


def get_conversations(session_id: str, limit: int = 100) -> List[Conversation]:
    """Get all conversations for a session"""
    return list(conversations_collection.find({"session_id": session_id}).sort("created_at", 1).limit(limit))  # type: ignore
