from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from ....core.security import get_current_user
from ....utils.db_utils import execute_query
from ....sql.queries.notification_queries import *

router = APIRouter()


@router.get("/")
async def get_user_notifications(
    unread_only: bool = False, current_user: dict = Depends(get_current_user)
):
    """Get user notifications"""
    try:
        query = GET_USER_NOTIFICATIONS_QUERY
        if unread_only:
            query = query.replace("ORDER BY", "WHERE read = FALSE ORDER BY")

        notifications = execute_query(
            query, (current_user["id"],), fetch_all=True
        )
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_notification(
    notification_data: dict, current_user: dict = Depends(get_current_user)
):
    """Create new notification"""
    try:
        result = execute_query(
            CREATE_NOTIFICATION_QUERY,
            (
                notification_data["user_id"],
                notification_data["type"],
                notification_data["message"],
            ),
            fetch_one=True,
        )
        return {
            "message": "Notification created successfully",
            "notification_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int, current_user: dict = Depends(get_current_user)
):
    """Mark notification as read"""
    try:
        result = execute_query(
            MARK_NOTIFICATION_READ_QUERY,
            (notification_id, current_user["id"]),
            fetch_one=True,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"message": "Notification marked as read"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int, current_user: dict = Depends(get_current_user)
):
    """Delete notification"""
    try:
        result = execute_query(
            DELETE_NOTIFICATION_QUERY,
            (notification_id, current_user["id"]),
            fetch_one=True,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Notification not found")
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
