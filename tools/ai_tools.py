"""
AI LangChain tools for Agent Angus.

These tools wrap the OpenAI functionality for use in LangChain agents.
"""
import sys
import os
import logging
from typing import Dict, Any, List, Optional
from langchain.tools import tool

# Add the parent directory to the path to import from original Angus
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Angus'))

try:
    from openai_utils import analyze_music, generate_response
except ImportError:
    # Fallback for when running without the original Angus code
    analyze_music = None
    generate_response = None

# Configure logging
logger = logging.getLogger(__name__)

@tool
def analyze_music_content(input_source: str, is_youtube_url: bool = False) -> Dict[str, Any]:
    """
    Analyze music using OpenAI for themes, genres, moods.
    
    Args:
        input_source: Either a path to an MP3 file or a YouTube URL
        is_youtube_url: Whether the input_source is a YouTube URL
        
    Returns:
        Dictionary with analysis results including themes, genres, moods, etc.
    """
    try:
        logger.info(f"Analyzing music content: {input_source} (YouTube: {is_youtube_url})")
        
        if analyze_music is None:
            raise ImportError("analyze_music function not available. Make sure the original Angus code is accessible.")
        
        # Use the original analyze_music function
        analysis_result = analyze_music(input_source, is_youtube_url)
        
        if "error" in analysis_result:
            logger.error(f"Music analysis failed: {analysis_result['error']}")
            return analysis_result
        
        logger.info(f"Music analysis completed successfully for: {input_source}")
        return analysis_result
        
    except Exception as e:
        error_msg = f"Error analyzing music content: {str(e)}"
        logger.error(error_msg)
        return {
            "error": "Music analysis failed",
            "details": error_msg,
            "input_source": input_source
        }

@tool
def generate_comment_response(comment_text: str, song_title: str, song_style: str = None) -> str:
    """
    Generate AI-powered response to YouTube comments.
    
    Args:
        comment_text: The text of the comment to respond to
        song_title: The title of the song
        song_style: Optional style information about the song
        
    Returns:
        Generated response text or error message
    """
    try:
        logger.info(f"Generating response for comment on '{song_title}': {comment_text[:50]}...")
        
        if generate_response is None:
            raise ImportError("generate_response function not available. Make sure the original Angus code is accessible.")
        
        # Use the original generate_response function
        response_text = generate_response(comment_text, song_title, song_style)
        
        if response_text:
            logger.info(f"Generated response: {response_text}")
            return response_text
        else:
            return "Failed to generate response"
            
    except Exception as e:
        error_msg = f"Error generating comment response: {str(e)}"
        logger.error(error_msg)
        return error_msg

@tool
def extract_music_metadata(audio_url: str) -> Dict[str, Any]:
    """
    Extract metadata from audio files.
    
    Args:
        audio_url: URL or path to the audio file
        
    Returns:
        Dictionary with extracted metadata
    """
    try:
        logger.info(f"Extracting metadata from audio: {audio_url}")
        
        # This is a placeholder implementation
        # In a real implementation, you would use audio processing libraries
        # to extract metadata like duration, bitrate, format, etc.
        
        metadata = {
            "url": audio_url,
            "status": "placeholder",
            "message": "Metadata extraction not implemented",
            "extracted_data": {
                "duration": "unknown",
                "format": "unknown",
                "bitrate": "unknown",
                "sample_rate": "unknown"
            }
        }
        
        logger.info(f"Metadata extraction completed (placeholder) for: {audio_url}")
        return metadata
        
    except Exception as e:
        error_msg = f"Error extracting metadata from {audio_url}: {str(e)}"
        logger.error(error_msg)
        return {
            "url": audio_url,
            "status": "error",
            "error": error_msg
        }

@tool
def analyze_comment_sentiment(comment_text: str) -> Dict[str, Any]:
    """
    Analyze the sentiment of a YouTube comment.
    
    Args:
        comment_text: The text of the comment to analyze
        
    Returns:
        Dictionary with sentiment analysis results
    """
    try:
        logger.info(f"Analyzing sentiment for comment: {comment_text[:50]}...")
        
        # This is a placeholder implementation
        # In a real implementation, you would use sentiment analysis
        # libraries or APIs to analyze the comment sentiment
        
        # Simple keyword-based sentiment analysis as placeholder
        positive_words = ['good', 'great', 'awesome', 'love', 'amazing', 'fantastic', 'excellent']
        negative_words = ['bad', 'terrible', 'hate', 'awful', 'horrible', 'worst', 'sucks']
        
        comment_lower = comment_text.lower()
        positive_count = sum(1 for word in positive_words if word in comment_lower)
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        result = {
            "comment": comment_text,
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "method": "simple_keyword_analysis"
        }
        
        logger.info(f"Sentiment analysis completed: {sentiment} ({confidence:.2f})")
        return result
        
    except Exception as e:
        error_msg = f"Error analyzing comment sentiment: {str(e)}"
        logger.error(error_msg)
        return {
            "comment": comment_text,
            "sentiment": "error",
            "error": error_msg
        }

@tool
def generate_song_description(song_data: Dict[str, Any]) -> str:
    """
    Generate a description for a song based on its data.
    
    Args:
        song_data: Dictionary containing song information
        
    Returns:
        Generated description text
    """
    try:
        logger.info(f"Generating description for song: {song_data.get('title', 'Unknown')}")
        
        title = song_data.get('title', 'Untitled Song')
        style = song_data.get('style', '')
        lyrics = song_data.get('lyrics', '')
        gpt_description = song_data.get('gpt_description', '')
        
        # Use existing GPT description if available
        if gpt_description:
            logger.info("Using existing GPT description")
            return gpt_description
        
        # Generate a basic description from available data
        description_parts = []
        
        if style:
            description_parts.append(f"A {style} song")
        else:
            description_parts.append("A musical composition")
            
        if lyrics:
            # Add a snippet of lyrics if available
            lyrics_snippet = lyrics[:200] + "..." if len(lyrics) > 200 else lyrics
            description_parts.append(f"\n\nLyrics:\n{lyrics_snippet}")
        
        description = " ".join(description_parts)
        
        logger.info(f"Generated description for '{title}'")
        return description
        
    except Exception as e:
        error_msg = f"Error generating song description: {str(e)}"
        logger.error(error_msg)
        return f"Description generation failed: {error_msg}"

@tool
def suggest_video_tags(song_data: Dict[str, Any]) -> List[str]:
    """
    Suggest tags for a YouTube video based on song data.
    
    Args:
        song_data: Dictionary containing song information
        
    Returns:
        List of suggested tags
    """
    try:
        logger.info(f"Suggesting tags for song: {song_data.get('title', 'Unknown')}")
        
        tags = []
        
        # Add style-based tags
        style = song_data.get('style', '')
        if style:
            # Split style by commas and clean up
            style_tags = [tag.strip() for tag in style.split(',') if tag.strip()]
            tags.extend(style_tags)
        
        # Add generic music tags
        tags.extend(['music', 'song', 'audio'])
        
        # Add AI-generated tag if this is AI music
        if 'ai' in song_data.get('title', '').lower() or 'generated' in song_data.get('title', '').lower():
            tags.append('ai music')
            tags.append('generated music')
        
        # Remove duplicates and limit to reasonable number
        unique_tags = list(dict.fromkeys(tags))[:10]  # YouTube allows up to 500 characters total
        
        logger.info(f"Generated {len(unique_tags)} tags for video")
        return unique_tags
        
    except Exception as e:
        error_msg = f"Error suggesting video tags: {str(e)}"
        logger.error(error_msg)
        return ['music', 'song']  # Fallback tags

# Tool list for easy import
AI_TOOLS = [
    analyze_music_content,
    generate_comment_response,
    extract_music_metadata,
    analyze_comment_sentiment,
    generate_song_description,
    suggest_video_tags
]
