"""
YouTube LangChain tools for Agent Angus.

These tools wrap the YouTube client functionality for use in LangChain agents.
"""
import sys
import os
import logging
from typing import Dict, Any, List, Optional
from langchain.tools import tool

# Add the parent directory to the path to import from original Angus
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Angus'))

try:
    from youtube_client import YouTubeClient
except ImportError:
    # Fallback for when running without the original Angus code
    YouTubeClient = None

# Configure logging
logger = logging.getLogger(__name__)

# Global YouTube client instance
_youtube_client = None

def get_youtube_client() -> YouTubeClient:
    """Get or create a YouTube client instance."""
    global _youtube_client
    if _youtube_client is None:
        if YouTubeClient is None:
            raise ImportError("YouTubeClient not available. Make sure the original Angus code is accessible.")
        _youtube_client = YouTubeClient()
    return _youtube_client

@tool
def upload_song_to_youtube(song_id: str, video_url: str, title: str, description: str, tags: List[str] = None) -> str:
    """
    Upload a single song to YouTube and return video ID.
    
    Args:
        song_id: The ID of the song in the database
        video_url: URL of the video file to upload
        title: Title of the video
        description: Description of the video
        tags: List of tags for the video
        
    Returns:
        YouTube video ID if successful, error message if failed
    """
    try:
        logger.info(f"Uploading song {song_id} to YouTube: {title}")
        
        youtube_client = get_youtube_client()
        youtube_id = youtube_client.upload_video(
            video_url=video_url,
            title=title,
            description=description,
            tags=tags or []
        )
        
        if youtube_id == "URL_EXPIRED":
            return f"Upload failed for song {song_id}: URL expired or inaccessible"
        elif youtube_id:
            logger.info(f"Successfully uploaded song {song_id} to YouTube: {youtube_id}")
            return youtube_id
        else:
            return f"Upload failed for song {song_id}: Unknown error"
            
    except Exception as e:
        error_msg = f"Error uploading song {song_id} to YouTube: {str(e)}"
        logger.error(error_msg)
        
        # Check if this is an upload limit exceeded error
        if "uploadLimitExceeded" in str(e) or "The user has exceeded the number of videos they may upload" in str(e):
            return f"Upload limit exceeded for song {song_id}"
        
        return error_msg

@tool
def fetch_youtube_comments(video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch comments for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        max_results: Maximum number of comments to retrieve
        
    Returns:
        List of comment data dictionaries
    """
    try:
        logger.info(f"Fetching comments for YouTube video: {video_id}")
        
        youtube_client = get_youtube_client()
        comments = youtube_client.fetch_comments(video_id, max_results)
        
        logger.info(f"Retrieved {len(comments)} comments for video {video_id}")
        return comments
        
    except Exception as e:
        error_msg = f"Error fetching comments for video {video_id}: {str(e)}"
        logger.error(error_msg)
        return []

@tool
def reply_to_youtube_comment(comment_id: str, reply_text: str) -> str:
    """
    Reply to a specific YouTube comment.
    
    Args:
        comment_id: The ID of the comment to reply to
        reply_text: The text of the reply
        
    Returns:
        Reply ID if successful, error message if failed
    """
    try:
        logger.info(f"Replying to YouTube comment: {comment_id}")
        
        youtube_client = get_youtube_client()
        reply_id = youtube_client.reply_to_comment(comment_id, reply_text)
        
        if reply_id:
            logger.info(f"Successfully replied to comment {comment_id}: {reply_id}")
            return reply_id
        else:
            return f"Failed to reply to comment {comment_id}"
            
    except Exception as e:
        error_msg = f"Error replying to comment {comment_id}: {str(e)}"
        logger.error(error_msg)
        return error_msg

@tool
def check_upload_quota() -> Dict[str, Any]:
    """
    Check YouTube API quota status.
    
    Returns:
        Dictionary with quota information
    """
    try:
        logger.info("Checking YouTube API quota status")
        
        # This is a placeholder implementation
        # In a real implementation, you would check the YouTube API quota
        # For now, we'll return a basic status
        
        return {
            "status": "available",
            "quota_remaining": "unknown",
            "daily_limit": "10000",
            "message": "Quota check not implemented - assuming available"
        }
        
    except Exception as e:
        error_msg = f"Error checking YouTube quota: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

@tool
def get_video_details(video_id: str) -> Dict[str, Any]:
    """
    Get details for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with video details
    """
    try:
        logger.info(f"Getting details for YouTube video: {video_id}")
        
        # This is a placeholder implementation
        # In a real implementation, you would use the YouTube API to get video details
        
        return {
            "video_id": video_id,
            "status": "placeholder",
            "message": "Video details retrieval not implemented"
        }
        
    except Exception as e:
        error_msg = f"Error getting video details for {video_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "video_id": video_id,
            "status": "error",
            "error": error_msg
        }

# Tool list for easy import
YOUTUBE_TOOLS = [
    upload_song_to_youtube,
    fetch_youtube_comments,
    reply_to_youtube_comment,
    check_upload_quota,
    get_video_details
]
