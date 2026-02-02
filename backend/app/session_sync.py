"""
Session Sync - Cloud-based session state synchronization.

This module enables:
1. Saving session state to cloud storage (Redis/Postgres)
2. Loading session state from cloud
3. Generating shareable session links
4. Real-time collaboration (future)
"""

from typing import Optional, Dict, Any, List
import logging
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

logger = logging.getLogger(__name__)

class SessionState(BaseModel):
    session_id: str
    user_id: str
    project_name: str
    messages: List[Dict[str, Any]]
    spec: Optional[Dict[str, Any]] = None
    file_changes: List[str] = []
    created_at: datetime
    updated_at: datetime

class SessionSyncService:
    """
    Service for syncing session state across users/devices.
    In production, this connects to Redis or PostgreSQL.
    """
    
    def __init__(self):
        # In-memory store for demo
        self._sessions: Dict[str, SessionState] = {}
        self._share_links: Dict[str, str] = {}  # link_id -> session_id

    async def save_session(self, session: SessionState) -> str:
        """Save session state and return session ID."""
        session.updated_at = datetime.utcnow()
        self._sessions[session.session_id] = session
        logger.info(
            "Session saved",
            extra={"session_id": session.session_id, "project": session.project_name},
        )
        return session.session_id

    async def load_session(self, session_id: str) -> Optional[SessionState]:
        """Load session state by ID."""
        session = self._sessions.get(session_id)
        if session:
            logger.info("Session loaded", extra={"session_id": session_id})
        else:
            logger.warning("Session not found", extra={"session_id": session_id})
        return session

    async def create_share_link(self, session_id: str) -> str:
        """Generate a shareable link for a session."""
        if session_id not in self._sessions:
            logger.warning("Session not found for share", extra={"session_id": session_id})
            raise ValueError(f"Session {session_id} not found")
        
        link_id = uuid.uuid4().hex[:12]
        self._share_links[link_id] = session_id
        
        # In production, this would be a full URL
        return f"forge://share/{link_id}"

    async def resolve_share_link(self, link_id: str) -> Optional[SessionState]:
        """Resolve a share link to its session."""
        session_id = self._share_links.get(link_id)
        if not session_id:
            return None
        return await self.load_session(session_id)

    async def list_user_sessions(self, user_id: str) -> List[SessionState]:
        """List all sessions for a user."""
        return [s for s in self._sessions.values() if s.user_id == user_id]

# Global instance
session_sync = SessionSyncService()

# --- API Helpers ---

async def save_current_session(
    session_id: str,
    user_id: str,
    project_name: str,
    messages: List[Dict[str, Any]],
    spec: Optional[Dict[str, Any]] = None,
    file_changes: List[str] | None = None,
) -> str:
    """Helper to save a session."""
    now = datetime.utcnow()
    session = SessionState(
        session_id=session_id,
        user_id=user_id,
        project_name=project_name,
        messages=messages,
        spec=spec,
        file_changes=file_changes or [],
        created_at=now,
        updated_at=now,
    )
    return await session_sync.save_session(session)

async def get_share_link(session_id: str) -> str:
    """Generate a share link for collaboration."""
    return await session_sync.create_share_link(session_id)
