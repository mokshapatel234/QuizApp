import asyncio
import os
from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from .utils import get_connection_manager, verify_token
from requests import Session

router = APIRouter()

manager = get_connection_manager()

async def get_current_user(token: str):
    """Helper function for auth with Firebase."""
    if not token:
        return ""
    try:
        user_info = verify_token(token)
        return user_info
    except HTTPException as e:
        raise e

