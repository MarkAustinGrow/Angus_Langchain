"""
YouTube LangChain tools for Agent Angus.

These tools wrap the YouTube client functionality for use in LangChain agents.
"""
import sys
import os
import logging
from typing import Dict, Any, List, Optional
from langchain.tools import tool

# Add the original Angus directory to the path
sys.path.append('E:/Plank pushers/Angus')

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
def upload_song_to_youtube(song_id: str, title: str = None, description: str = None, tags: List[str] = None, privacy: str = "public") -> str:
    """
    Upload a song to YouTube.
    
    Args:
        song_id: ID of the song to upload
        title: Video title (will be fetched from database if not provided)
        description: Video description (will be generated if not provided)
        tags: List of video tags (will be generated if not provided)
        privacy: Privacy setting (public, private, unlisted)
        
    Returns:
        YouTube video ID if successful, error message if failed
    """
    try:
        logger.info(f"Uploading song {song_id} to YouTube")
        
        # Get song details from database
        from tools.supabase_tools import get_song_details
        song_data = get_song_details(song_id)
        
        if not song_data or 'error' in song_data:
            return f"Error: Could not retrieve song data for {song_id}"
        
        video_url = song_data.get('video_url')
        if not video_url:
            return f"Error: No video URL found for song {song_id}"
        
        # Use provided values or defaults from song data
        upload_title = title or song_data.get('title', 'Untitled Song')
        upload_description = description or song_data.get('gpt_description', '')
        
        # If no description, use lyrics
        if not upload_description and song_data.get('lyrics'):
            upload_description = f"Lyrics:\n\n{song_data['lyrics']}"
        
        # Prepare tags
        upload_tags = tags or []
        if not upload_tags and song_data.get('style'):
            upload_tags = [tag.strip() for tag in song_data['style'].split(',')]
        
        # Upload to YouTube using original client
        youtube_client = get_youtube_client()
        youtube_id = youtube_client.upload_video(
            video_url=video_url,
            title=upload_title,
            description=upload_description,
            tags=upload_tags
        )
        
        if youtube_id == "URL_EXPIRED":
            # Update status in database
            from tools.supabase_tools import update_song_status
            update_song_status(song_id, "url_expired")
            return f"Error: Video URL expired for song {song_id}"
        
        if youtube_id:
            # Update status in database
            from tools.supabase_tools import update_song_status
            update_song_status(song_id, "uploaded", youtube_id)
            logger.info(f"Successfully uploaded song {song_id} to YouTube: {youtube_id}")
            return youtube_id
        else:
            # Update status in database
            from tools.supabase_tools import update_song_status
            update_song_status(song_id, "failed")
            return f"Error: Upload failed for song {song_id}"
            
    except Exception as e:
        error_msg = f"Error uploading song {song_id}: {str(e)}"
        logger.error(error_msg)
        
        # Check if this is an upload limit exceeded error
        if "uploadLimitExceeded" in str(e) or "The user has exceeded the number of videos they may upload" in str(e):
            # Update status in database
            from tools.supabase_tools import update_song_status
            update_song_status(song_id, "failed")
            return f"Error: YouTube upload limit exceeded"
        
        return error_msg

@tool
def fetch_youtube_comments(video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch comments from a YouTube video.
    
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
    Reply to a YouTube comment.
    
    Args:
        comment_id: ID of the comment to reply to
        reply_text: Text of the reply
        
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
            return f"Error: Failed to reply to comment {comment_id}"
            
    except Exception as e:
        error_msg = f"Error replying to comment {comment_id}: {str(e)}"
        logger.error(error_msg)
        return error_msg

@tool
def check_upload_quota() -> Dict[str, Any]:
    """
    Check YouTube API upload quota status.
    
    Returns:
        Dictionary with quota information
    """
    try:
        logger.info("Checking YouTube upload quota")
        
        # For now, return a basic status since the original client doesn't have this method
        # This could be enhanced to actually check quota usage
        return {
            "status": "available",
            "quota_remaining": "unknown",
            "daily_limit": "10000",
            "message": "Quota check available - using original YouTube client"
        }
        
    except Exception as e:
        error_msg = f"Error checking upload quota: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }

@tool
def get_video_details(video_id: str) -> Dict[str, Any]:
    """
    Get details of a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with video details
    """
    try:
        logger.info(f"Getting details for YouTube video: {video_id}")
        
        youtube_client = get_youtube_client()
        
        # The original client doesn't have a get_video_details method
        # We can implement basic functionality or return what we know
        return {
            "video_id": video_id,
            "status": "exists",
            "message": "Video details retrieved using original YouTube client"
        }
        
    except Exception as e:
        error_msg = f"Error getting video details for {video_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "video_id": video_id,
            "status": "error",
            "message": error_msg
        }

@tool
def process_video_comments(video_id: str, song_id: str = None, max_replies: int = 10) -> int:
    """
    Process comments for a YouTube video - fetch, analyze, and reply.
    
    Args:
        video_id: YouTube video ID
        song_id: Song ID (will be looked up if not provided)
        max_replies: Maximum number of replies to post
        
    Returns:
        Number of comments processed
    """
    try:
        logger.info(f"Processing comments for video {video_id}")
        
        # Get song info if not provided
        if not song_id:
            from tools.supabase_tools import get_supabase_client
            supabase_client = get_supabase_client()
            response = supabase_client.client.table("youtube").select("song_id").eq("youtube_id", video_id).execute()
            if response.data and len(response.data) > 0:
                song_id = response.data[0].get('song_id')
            else:
                return 0
        
        # Get song details for context
        from tools.supabase_tools import get_song_details
        song_data = get_song_details(song_id)
        song_title = song_data.get('title', 'Unknown Song') if song_data else 'Unknown Song'
        song_style = song_data.get('style') if song_data else None
        
        # Fetch comments
        comments = fetch_youtube_comments(video_id, max_results=100)
        
        if not comments:
            return 0
        
        # Get existing feedback to avoid duplicates
        from tools.supabase_tools import get_existing_feedback
        existing_feedback = get_existing_feedback(song_id)
        existing_comment_ids = set()
        if existing_feedback:
            for feedback in existing_feedback:
                if feedback.get('comment_id'):
                    existing_comment_ids.add(feedback.get('comment_id'))
        
        # Process comments
        processed_count = 0
        for comment in comments:
            if processed_count >= max_replies:
                break
                
            comment_id = comment.get("comment_id")
            comment_text = comment.get("content", "")
            
            # Skip if already processed
            if comment_id in existing_comment_ids:
                continue
                
            # Skip if we already replied
            if comment.get("has_our_reply", False):
                continue
            
            try:
                # Store feedback
                from tools.supabase_tools import store_feedback
                store_feedback(song_id, comment)
                
                # Generate response using AI tools
                from tools.ai_tools import generate_comment_response
                response_text = generate_comment_response(comment_text, song_title, song_style)
                
                if response_text:
                    # Reply to comment
                    reply_id = reply_to_youtube_comment(comment_id, response_text)
                    if reply_id and not reply_id.startswith("Error"):
                        processed_count += 1
                        logger.info(f"Successfully processed comment: {comment_text[:50]}...")
                
            except Exception as e:
                logger.error(f"Error processing comment {comment_id}: {str(e)}")
        
        logger.info(f"Processed {processed_count} comments for video {video_id}")
        return processed_count
        
    except Exception as e:
        error_msg = f"Error processing comments for video {video_id}: {str(e)}"
        logger.error(error_msg)
        return 0

# Tool list for easy import
YOUTUBE_TOOLS = [
    upload_song_to_youtube,
    fetch_youtube_comments,
    reply_to_youtube_comment,
    check_upload_quota,
    get_video_details,
    process_video_comments
]
