"""
Main Entry Point for Home Assistant Chatbot
Supports both Telegram bot and web interface
"""
import os
import sys
from pathlib import Path
from threading import Thread
from flask import Flask
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import ConfigManager, setup_logging
from core import HomeChatbot
from handlers.telegram_handler import TelegramBotHandler

# Load environment variables
load_dotenv()

# Flask app for health checks (required by some hosting services)
app = Flask(__name__)

@app.route('/')
def index():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "MarIA - Smart Home Assistant",
        "message": "🤖 MarIA is active!"
    }, 200

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy"}, 200

def run_flask(config):
    """Run Flask web server"""
    app.run(
        host=config.web.host,
        port=config.web.port,
        debug=config.web.debug
    )

def main():
    """Main function"""
    print("=" * 60)
    print("🤖 MarIA - Your Smart Home Assistant")
    print("=" * 60)
    
    # Load configuration
    config_path = os.getenv('CONFIG_PATH', None)
    config_manager = ConfigManager(config_path)
    config = config_manager.config
    
    print(f"📋 Configuration loaded from: {config_manager.config_path}")
    print(f"🌍 Environment: {config.environment}")
    print(f"📦 Version: {config.version}")
    
    # Setup logging
    logger = setup_logging(config.logging)
    log = logger.get_logger("Main")
    
    log.info("Starting MarIA - Your Smart Home Assistant...")
    
    # Validate configuration
    is_valid, errors = config_manager.validate_config()
    if not is_valid:
        log.error("Configuration validation failed:")
        for error in errors:
            log.error(f"  - {error}")
        print("\n⚠️ Configuration errors found. Please check your settings.")
        print("\n📝 Required environment variables:")
        print(config_manager.get_env_template())
        sys.exit(1)
    
    log.info("✅ Configuration validated successfully")
    
    # Initialize chatbot
    try:
        log.info("Initializing chatbot core...")
        chatbot = HomeChatbot(config)
        log.info("✅ Chatbot initialized successfully")
        
        # Display stats
        stats = chatbot.get_stats()
        if stats['rag'].get('enabled'):
            log.info(f"📚 Knowledge base: {stats['rag']['total_documents']} documents")
        else:
            log.info("📚 RAG system disabled - using base LLM knowledge")
        
    except Exception as e:
        log.error(f"❌ Failed to initialize chatbot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Start web server in background (for health checks)
    if config.web.enabled:
        log.info(f"🌐 Starting web server on {config.web.host}:{config.web.port}")
        web_thread = Thread(target=run_flask, args=(config,), daemon=True)
        web_thread.start()
    
    # Start Telegram bot
    if config.telegram.enabled:
        log.info("🤖 Starting Telegram bot...")
        try:
            telegram_handler = TelegramBotHandler(chatbot, config)
            log.info("✅ Telegram bot is running!")
            log.info("Press Ctrl+C to stop")
            print("\n" + "=" * 60)
            print("✅ BOT IS RUNNING!")
            print("=" * 60 + "\n")
            telegram_handler.run()
        except Exception as e:
            log.error(f"❌ Failed to start Telegram bot: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        log.info("Telegram bot disabled in configuration")
        if config.web.enabled:
            log.info("Web server is running. Press Ctrl+C to stop")
            # Keep the program running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                log.info("Shutting down...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)