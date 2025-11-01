"""
Utility functions for the chatbot application
"""
import os
import hashlib
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json


def generate_document_id(content: str, category: str = "general") -> str:
    """Generate unique document ID based on content hash"""
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{category}_{timestamp}_{content_hash}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def ensure_directory(path: str) -> bool:
    """Ensure directory exists, create if not"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = {}
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if user is allowed to make a call"""
        now = datetime.now()
        user_calls = self.calls.get(user_id, [])
        
        # Remove old calls outside time window
        cutoff_time = now - timedelta(seconds=self.time_window)
        user_calls = [call_time for call_time in user_calls if call_time > cutoff_time]
        
        # Check if under limit
        if len(user_calls) < self.max_calls:
            user_calls.append(now)
            self.calls[user_id] = user_calls
            return True
        
        return False
    
    def get_reset_time(self, user_id: str) -> Optional[datetime]:
        """Get when rate limit resets for user"""
        user_calls = self.calls.get(user_id, [])
        if not user_calls:
            return None
        
        oldest_call = min(user_calls)
        return oldest_call + timedelta(seconds=self.time_window)


class MemoryCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.cache = {}
        self.default_ttl = default_ttl
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value with TTL"""
        if ttl is None:
            ttl = self.default_ttl
        
        expire_time = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = {
            'value': value,
            'expire_time': expire_time
        }
    
    def get(self, key: str) -> Any:
        """Get cache value, return None if expired or not found"""
        if key not in self.cache:
            return None
        
        cached_item = self.cache[key]
        if datetime.now() > cached_item['expire_time']:
            del self.cache[key]
            return None
        
        return cached_item['value']
    
    def delete(self, key: str) -> bool:
        """Delete cache key"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired items, return count of removed items"""
        now = datetime.now()
        expired_keys = [
            key for key, item in self.cache.items()
            if now > item['expire_time']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)


async def retry_async(func, max_retries: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    """Retry async function with exponential backoff"""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = delay * (backoff_factor ** attempt)
                await asyncio.sleep(wait_time)
            continue
    
    raise last_exception


def safe_json_load(file_path: str, default: Any = None) -> Any:
    """Safely load JSON file, return default if error"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def safe_json_save(data: Any, file_path: str) -> bool:
    """Safely save data to JSON file"""
    try:
        # Ensure directory exists
        ensure_directory(os.path.dirname(file_path))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase"""
    return os.path.splitext(filename)[1].lower()


def is_pdf_file(filename: str) -> bool:
    """Check if file is PDF"""
    return get_file_extension(filename) == '.pdf'


def validate_environment_variables(required_vars: List[str]) -> tuple[bool, List[str]]:
    """Validate that required environment variables are set"""
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars


def create_error_response(error_type: str, message: str, details: Optional[Dict] = None) -> Dict:
    """Create standardized error response"""
    response = {
        'success': False,
        'error': {
            'type': error_type,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return response


def create_success_response(data: Any = None, message: str = "Success") -> Dict:
    """Create standardized success response"""
    response = {
        'success': True,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    return response