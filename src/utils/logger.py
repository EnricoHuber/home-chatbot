"""
Logging System
Provides structured logging for the application
"""
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional
from utils.config_manager import LoggingConfig


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        if hasattr(record, 'color') and record.color:
            color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{color}{record.levelname}{self.RESET}"
            record.name = f"{color}{record.name}{self.RESET}"
        
        return super().format(record)


class ChatbotLogger:
    """Centralized logging system for the chatbot"""
    
    def __init__(self, config: LoggingConfig):
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory
        log_dir = os.path.dirname(self.config.log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure root logger
        logging.root.setLevel(getattr(logging, self.config.level.upper()))
        
        # Remove existing handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.addFilter(lambda record: setattr(record, 'color', True) or True)
        logging.root.addHandler(console_handler)
        
        # File handler with rotation
        if self.config.log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)-15s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logging.root.addHandler(file_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger instance"""
        return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def log_method_call(self, method_name: str, **kwargs):
        """Log method call with parameters"""
        if self.logger.isEnabledFor(logging.DEBUG):
            params = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
            self.log_debug(f"Calling {method_name}({params})")
    
    def log_debug(self, message: str):
        """Log debug message"""
        self.logger.debug(f"🔍 {message}")
    
    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(f"ℹ️ {message}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(f"⚠️ {message}")
    
    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error message"""
        self.logger.error(f"❌ {message}")
        if exception:
            self.logger.exception(exception)
    
    def log_success(self, message: str):
        """Log success message"""
        self.logger.info(f"✅ {message}")


def setup_logging(config: LoggingConfig) -> ChatbotLogger:
    """Setup application logging"""
    return ChatbotLogger(config)


# Performance logging decorator
def log_performance(logger: logging.Logger):
    """Decorator to log method execution time"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.debug(f"⏱️ {func.__name__} executed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"❌ {func.__name__} failed after {execution_time:.3f}s: {e}")
                raise
        return wrapper
    return decorator