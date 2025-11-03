"""
Configuration Management System
Handles loading and validation of configuration files
"""
import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LLMConfig:
    """LLM Configuration"""
    provider: str = "groq"
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.7
    max_tokens: int = 500
    api_key_env: str = "GROQ_API_KEY"


@dataclass
class RAGConfig:
    """RAG Configuration"""
    enabled: bool = True
    storage_type: str = "chromadb"  # chromadb or supabase
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_path: str = "./chroma_db"
    collection_name: str = "home_assistant"
    max_search_results: int = 3
    similarity_threshold: float = 0.7


@dataclass
class TelegramConfig:
    """Telegram Bot Configuration"""
    enabled: bool = True
    token_env: str = "TELEGRAM_BOT_TOKEN"
    allowed_users: Optional[list] = None
    rate_limit_messages: int = 20
    rate_limit_window: int = 60  # seconds


@dataclass
class WebConfig:
    """Web Interface Configuration"""
    enabled: bool = True
    host: str = "0.0.0.0"
    port: int = 10000
    debug: bool = False


@dataclass
class LoggingConfig:
    """Logging Configuration"""
    level: str = "INFO"
    verbose: bool = False
    log_file: str = "./logs/chatbot.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class AppConfig:
    """Main Application Configuration"""
    app_name: str = "Home Assistant Chatbot"
    version: str = "1.0.0"
    environment: str = "development"
    llm: LLMConfig = None
    rag: RAGConfig = None
    telegram: TelegramConfig = None
    web: WebConfig = None
    logging: LoggingConfig = None

    def __post_init__(self):
        if self.llm is None:
            self.llm = LLMConfig()
        if self.rag is None:
            self.rag = RAGConfig()
        if self.telegram is None:
            self.telegram = TelegramConfig()
        if self.web is None:
            self.web = WebConfig()
        if self.logging is None:
            self.logging = LoggingConfig()


class ConfigManager:
    """Configuration Manager"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self.load_config()

    def _get_default_config_path(self) -> str:
        """Get default configuration path based on environment"""
        env = os.getenv("ENVIRONMENT", "development").lower()
        if env in ["production", "prod"]:
            return "./configs/production_config.json"
        elif env in ["test", "testing"]:
            return "./configs/test_small_model.json"
        else:  # development, dev, or any other value
            return "./configs/base_config.json"

    def load_config(self) -> AppConfig:
        """Load configuration from file"""
        if not os.path.exists(self.config_path):
            print(f"⚠️ Config file not found: {self.config_path}")
            print("🔧 Creating default configuration...")
            return self._create_default_config()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            
            return self._parse_config(config_data)
        
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            print("🔧 Using default configuration...")
            return self._create_default_config()

    def _parse_config(self, config_data: Dict[str, Any]) -> AppConfig:
        """Parse configuration dictionary into AppConfig"""
        llm_data = config_data.get("llm", {})
        rag_data = config_data.get("rag", {})
        telegram_data = config_data.get("telegram", {})
        web_data = config_data.get("web", {})
        logging_data = config_data.get("logging", {})

        return AppConfig(
            app_name=config_data.get("app_name", "Home Assistant Chatbot"),
            version=config_data.get("version", "1.0.0"),
            environment=config_data.get("environment", "development"),
            llm=LLMConfig(**llm_data),
            rag=RAGConfig(**rag_data),
            telegram=TelegramConfig(**telegram_data),
            web=WebConfig(**web_data),
            logging=LoggingConfig(**logging_data)
        )

    def _create_default_config(self) -> AppConfig:
        """Create default configuration"""
        return AppConfig()

    def save_config(self, config: AppConfig = None) -> bool:
        """Save configuration to file"""
        if config is None:
            config = self.config

        try:
            config_dict = {
                "app_name": config.app_name,
                "version": config.version,
                "environment": config.environment,
                "llm": {
                    "provider": config.llm.provider,
                    "model": config.llm.model,
                    "temperature": config.llm.temperature,
                    "max_tokens": config.llm.max_tokens,
                    "api_key_env": config.llm.api_key_env
                },
                "rag": {
                    "enabled": config.rag.enabled,
                    "embedding_model": config.rag.embedding_model,
                    "chroma_path": config.rag.chroma_path,
                    "collection_name": config.rag.collection_name,
                    "max_search_results": config.rag.max_search_results,
                    "similarity_threshold": config.rag.similarity_threshold
                },
                "telegram": {
                    "enabled": config.telegram.enabled,
                    "token_env": config.telegram.token_env,
                    "allowed_users": config.telegram.allowed_users,
                    "rate_limit_messages": config.telegram.rate_limit_messages,
                    "rate_limit_window": config.telegram.rate_limit_window
                },
                "web": {
                    "enabled": config.web.enabled,
                    "host": config.web.host,
                    "port": config.web.port,
                    "debug": config.web.debug
                },
                "logging": {
                    "level": config.logging.level,
                    "verbose": config.logging.verbose,
                    "log_file": config.logging.log_file,
                    "max_file_size": config.logging.max_file_size,
                    "backup_count": config.logging.backup_count
                }
            }

            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False

    def validate_config(self) -> tuple[bool, list]:
        """Validate configuration and return errors if any"""
        errors = []
        
        # Validate LLM config
        if not self.config.llm.provider:
            errors.append("LLM provider not specified")
        
        if not self.config.llm.model:
            errors.append("LLM model not specified")
        
        # Check environment variables
        if self.config.llm.provider == "groq":
            if not os.getenv(self.config.llm.api_key_env):
                errors.append(f"Environment variable {self.config.llm.api_key_env} not set")
        
        if self.config.telegram.enabled:
            if not os.getenv(self.config.telegram.token_env):
                errors.append(f"Environment variable {self.config.telegram.token_env} not set")
        
        # Validate paths
        if self.config.rag.enabled:
            try:
                os.makedirs(self.config.rag.chroma_path, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create chroma_path: {e}")
        
        return len(errors) == 0, errors

    def get_env_template(self) -> str:
        """Get environment variables template"""
        return f"""# Environment Variables for {self.config.app_name}
# Copy this to .env file and fill in your values

# LLM Configuration
{self.config.llm.api_key_env}=your_groq_api_key_here

# Telegram Bot Configuration  
{self.config.telegram.token_env}=your_telegram_bot_token_here

# Environment
ENVIRONMENT={self.config.environment}
"""