# main.py - Bot Telegram principale
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from chatbot_core import HomeChatbot
from dotenv import load_dotenv

from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "🏠 Home Chatbot attivo!", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000)

load_dotenv()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Inizializza il chatbot
chatbot = HomeChatbot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    await update.message.reply_text(
        '🏠 Ciao! Sono il tuo assistente domestico.\n'
        'Puoi chiedermi:\n'
        '• Informazioni sulle utenze\n'
        '• Metodi di pulizia naturali\n'
        '• Consigli per la casa\n\n'
        'Invia /help per più comandi!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    help_text = """
🤖 **Comandi disponibili:**
/start - Avvia il bot
/help - Mostra questo messaggio
/upload - Carica un documento PDF
/info - Info sul database conoscenze

💬 **Esempi di domande:**
- "Come pulire il forno naturalmente?"
- "Quando scade il contratto dell'elettricità?"
- "Ricetta detergente fai da te"
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce i messaggi dell'utente"""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    try:
        # Invia "typing..." per mostrare che il bot sta elaborando
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Ottieni risposta dal chatbot
        response = await chatbot.get_response(user_message, user_id)
        
        # Invia la risposta
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Errore nel processare il messaggio: {e}")
        await update.message.reply_text("Scusa, ho avuto un problema. Riprova!")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce i documenti PDF caricati"""
    if update.message.document and update.message.document.mime_type == 'application/pdf':
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_document")
            
            # Scarica il file
            file = await context.bot.get_file(update.message.document.file_id)
            file_path = f"temp_{update.message.document.file_name}"
            await file.download_to_drive(file_path)
            
            # Processa il PDF
            success = await chatbot.add_document(file_path)
            
            if success:
                await update.message.reply_text("✅ Documento aggiunto al database delle conoscenze!")
            else:
                await update.message.reply_text("❌ Errore nel processare il documento.")
                
            # Rimuovi file temporaneo
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            logger.error(f"Errore nel processare PDF: {e}")
            await update.message.reply_text("Errore nel caricare il documento.")

def main() -> None:
    """Avvia il bot"""
    # Token del bot Telegram (ottieni da @BotFather)
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("ERRORE: Imposta TELEGRAM_BOT_TOKEN nelle variabili d'ambiente!")
        return
    
    # Crea l'applicazione
    application = Application.builder().token(TOKEN).build()
    
    # Aggiungi handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    
    # Avvia il bot
    print("🤖 Bot avviato! Premi Ctrl+C per fermare.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    main()