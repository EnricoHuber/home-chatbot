"""
Telegram Bot Handler
Handles all Telegram bot interactions
"""
import os
from typing import Optional
from telegram import Update, BotCommand
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

from core import HomeChatbot
from utils import LoggerMixin
from utils.helpers import RateLimiter


class TelegramBotHandler(LoggerMixin):
    """Telegram Bot Handler"""
    
    def __init__(self, chatbot: HomeChatbot, config):
        self.chatbot = chatbot
        self.config = config.telegram
        self.rate_limiter = RateLimiter(
            max_calls=self.config.rate_limit_messages,
            time_window=self.config.rate_limit_window
        )
        self.application = None
        self.log_info("Telegram bot handler initialized")
    
    def is_user_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to use the bot"""
        if self.config.allowed_users is None:
            return True
        return user_id in self.config.allowed_users
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.first_name or "utente"
        
        self.log_info(f"Start command from user {user_id}")
        
        if not self.is_user_allowed(user_id):
            await update.message.reply_text("⚠️ Non sei autorizzato a usare questo bot.")
            return
        
        welcome_message = f"""🏠 Ciao {username}! Sono il tuo assistente domestico.

Posso aiutarti con:
• 🧹 Consigli per la pulizia naturale
• 💡 Gestione delle utenze domestiche
• 🔧 Manutenzione della casa
• 📋 Organizzazione domestica

💡 **Posso imparare da te!**
Usa /addknowledge per insegnarmi informazioni sulla tua casa, oppure inviami documenti PDF.

Fai una domanda o usa /help per vedere tutti i comandi disponibili!"""
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = """🤖 **Comandi disponibili:**

**📋 Comandi Base:**
/start - Avvia il bot
/help - Mostra questo messaggio
/info - Informazioni sul bot

**📊 Monitoraggio:**
/stats - Statistiche del database conoscenze
/usage - Utilizzo servizi in tempo reale
/resources - Link a tutte le dashboard

**📚 Gestione Conoscenze:**
/addknowledge - Aggiungi nuova conoscenza

💬 **Esempi di domande:**
• "Come pulire il forno naturalmente?"
• "Come risparmiare energia in casa?"
• "Ricetta per detergente naturale"
• "Come rimuovere il calcare?"
• "Consigli per la manutenzione del condizionatore"

📝 **Aggiungere conoscenze:**
1. **Testo**: Usa /addknowledge seguito dal testo
   Esempio: `/addknowledge Il contratto luce scade il 31/12/2025`

2. **PDF**: Invia un file PDF direttamente
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /stats command"""
        try:
            stats = self.chatbot.get_stats()
            
            rag_info = stats.get('rag', {})
            if rag_info.get('enabled'):
                total_docs = rag_info.get('total_documents', 0)
                categories = rag_info.get('categories', {})
                cat_text = "\n".join([f"  • {cat}: {count}" for cat, count in categories.items()])
                
                stats_text = f"""📊 **Statistiche Bot**

📚 **Database Conoscenze:**
  • Totale documenti: {total_docs}
  • Categorie:
{cat_text}

🤖 **Informazioni:**
  • Versione: {stats.get('version', 'N/A')}
  • Ambiente: {stats.get('environment', 'N/A')}
"""
            else:
                stats_text = """📊 **Statistiche Bot**

⚠️ Database RAG non attivo
Usando solo conoscenza base del modello.
"""
            
            await update.message.reply_text(stats_text, parse_mode='Markdown')
            
        except Exception as e:
            self.log_error(f"Error getting stats: {e}", e)
            await update.message.reply_text("❌ Errore nel recuperare le statistiche.")
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /info command"""
        info_text = """ℹ️ **Informazioni sul Bot**

Sono un assistente domestico intelligente che utilizza:
• 🧠 AI per comprendere le tue domande
• 📚 Database di conoscenze specializzato
• 🔍 Ricerca semantica per trovare info rilevanti

Le mie specialità:
• Pulizie naturali ed ecologiche
• Gestione utenze e risparmio energetico
• Manutenzione domestica
• Organizzazione della casa

📚 **Puoi insegnarmi cose nuove:**
• Usa /addknowledge per aggiungere testo
• Inviami documenti PDF
• Tutto viene salvato e usato per risponderti meglio!
"""
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def resources_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /resources command - show service dashboards and links"""
        resources_text = """🔗 **Risorse e Dashboard**

📊 **Monitoraggio Servizi:**

**🚂 Railway (Hosting Bot)**
📍 Dashboard: https://railway.app/dashboard
• Visualizza log in tempo reale
• Monitora utilizzo CPU/RAM
• Controlla credito rimanente ($5/mese)
• Gestisci variabili ambiente

**🗄️ Supabase (Database)**
📍 Dashboard: https://supabase.com/dashboard
• Table Editor: Visualizza documenti salvati
• SQL Editor: Query personalizzate
• Settings → Usage: Controlla spazio usato (500MB free)
• Settings → API: Chiavi e documentazione

**🤖 Groq (AI/LLM)**
📍 Console: https://console.groq.com
• Settings → Limits: Visualizza rate limits
• Usage: 14,400 richieste/giorno (free tier)
• API Keys: Gestisci chiavi API

━━━━━━━━━━━━━━━━━━━━━━
📈 **Limiti Attuali:**
• Railway: $5 credito/mese (~500 ore uptime)
• Supabase: 500MB storage (0.002% usato)
• Groq: 14,400 richieste/giorno

💡 Usa /usage per vedere l'utilizzo in tempo reale!
"""
        await update.message.reply_text(resources_text, parse_mode='Markdown', disable_web_page_preview=True)
    
    async def usage_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /usage command - fetch real usage data from APIs"""
        await update.message.reply_text("🔄 Recupero informazioni sull'utilizzo...")
        
        try:
            # Get Supabase stats
            supabase_stats = self.chatbot.rag_system.storage.get_stats() if hasattr(self.chatbot.rag_system, 'storage') else {}
            
            # Get environment
            environment = os.getenv('ENVIRONMENT', 'development')
            
            # Build usage report
            usage_text = f"""📊 **Report Utilizzo Servizi**

**🗄️ Supabase (Database Conoscenze)**
• Backend: {supabase_stats.get('storage_backend', 'N/A')}
• Documenti totali: {supabase_stats.get('total', 0)}
• Spazio stimato: ~{supabase_stats.get('total', 0) * 2} KB / 500 MB
• Stato: ✅ Operativo

**📚 Categorie Documenti:**"""
            
            # Add categories
            categories = supabase_stats.get('by_category', {})
            if categories:
                for cat, count in categories.items():
                    usage_text += f"\n  • {cat}: {count} documenti"
            else:
                usage_text += "\n  • Nessuna categoria"
            
            usage_text += f"""

**🚂 Railway (Hosting)**
• Ambiente: {environment}
• Stato: ✅ Online
• Uptime: Bot attivo
• Health check: http://localhost:10000/health

**🤖 Groq (AI Model)**
• Modello: {self.chatbot.config.llm.model}
• Rate limit: 30 req/minuto
• Daily limit: 14,400 req/giorno
• Stato: ✅ Operativo

━━━━━━━━━━━━━━━━━━━━━━
💡 **Suggerimenti:**
• Controlla Railway dashboard per utilizzo CPU/RAM
• Visita Supabase dashboard per vedere i dati
• Usa /resources per link diretti alle dashboard
"""
            
            await update.message.reply_text(usage_text, parse_mode='Markdown')
            
        except Exception as e:
            self.log_error(f"Error getting usage info: {e}", e)
            await update.message.reply_text(
                "❌ Errore nel recuperare le informazioni sull'utilizzo.\n"
                "Usa /resources per accedere alle dashboard manualmente."
            )
    
    async def addknowledge_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /addknowledge command to add knowledge directly"""
        user_id = update.effective_user.id
        
        if not self.is_user_allowed(user_id):
            await update.message.reply_text("⚠️ Non sei autorizzato a usare questo bot.")
            return
        
        # Get the text after the command
        if not context.args:
            await update.message.reply_text(
                """📚 **Come aggiungere conoscenza:**

**Formato:**
`/addknowledge [categoria] testo della conoscenza`

**Categorie disponibili:**
• pulizia
• utenze
• manutenzione
• casa
• generale (default)

**Esempi:**
`/addknowledge utenze Il contratto luce scade il 31/12/2025`
`/addknowledge pulizia Per il parquet usare solo panni umidi`
`/addknowledge Il garage si chiude con il codice 1234`

Se non specifichi la categoria, verrà usata "generale".""",
                parse_mode='Markdown'
            )
            return
        
        try:
            # Parse category and content
            categories = ['pulizia', 'utenze', 'manutenzione', 'casa', 'generale']
            first_word = context.args[0].lower()
            
            if first_word in categories:
                category = first_word
                content = ' '.join(context.args[1:])
            else:
                category = 'generale'
                content = ' '.join(context.args)
            
            if not content or len(content.strip()) < 10:
                await update.message.reply_text(
                    "⚠️ Il contenuto è troppo corto. Scrivi almeno 10 caratteri."
                )
                return
            
            # Add to knowledge base
            if self.chatbot.rag_system.config.enabled:
                doc_id = self.chatbot.rag_system.add_knowledge(content, category)
                
                if doc_id:
                    await update.message.reply_text(
                        f"""✅ **Conoscenza aggiunta!**

📁 Categoria: {category}
📝 Contenuto: {content[:100]}{'...' if len(content) > 100 else ''}
🆔 ID: {doc_id}

Ora posso usare questa informazione per rispondere alle domande!"""
                    )
                    self.log_success(f"Knowledge added by user {user_id}: {doc_id}")
                else:
                    await update.message.reply_text("❌ Errore nell'aggiungere la conoscenza.")
            else:
                await update.message.reply_text(
                    "⚠️ Il sistema RAG è disabilitato. Non posso aggiungere conoscenze."
                )
                
        except Exception as e:
            self.log_error(f"Error adding knowledge: {e}", e)
            await update.message.reply_text(
                "❌ Errore nell'aggiungere la conoscenza. Riprova!"
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle user messages"""
        user_message = update.message.text
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self.is_user_allowed(user_id):
            await update.message.reply_text("⚠️ Non sei autorizzato a usare questo bot.")
            return
        
        # Check rate limit
        if not self.rate_limiter.is_allowed(str(user_id)):
            reset_time = self.rate_limiter.get_reset_time(str(user_id))
            await update.message.reply_text(
                f"⚠️ Troppi messaggi! Riprova tra qualche secondo."
            )
            return
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="typing"
            )
            
            # Get response from chatbot
            self.log_info(f"Processing message from user {user_id}: {user_message[:50]}...")
            response = await self.chatbot.get_response(user_message, str(user_id))
            
            # Send response
            await update.message.reply_text(response)
            self.log_success(f"Response sent to user {user_id}")
            
        except Exception as e:
            self.log_error(f"Error processing message: {e}", e)
            await update.message.reply_text(
                "⚠️ Scusa, ho avuto un problema tecnico. Riprova tra poco!"
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle PDF documents"""
        user_id = update.effective_user.id
        
        if not self.is_user_allowed(user_id):
            await update.message.reply_text("⚠️ Non sei autorizzato a usare questo bot.")
            return
        
        if not update.message.document or update.message.document.mime_type != 'application/pdf':
            await update.message.reply_text("⚠️ Per favore invia solo file PDF.")
            return
        
        try:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action="upload_document"
            )
            
            # Download file
            file = await context.bot.get_file(update.message.document.file_id)
            file_path = f"temp_{update.message.document.file_name}"
            await file.download_to_drive(file_path)
            
            self.log_info(f"Processing PDF: {file_path}")
            
            # Process PDF
            success = await self.chatbot.add_document(file_path)
            
            if success:
                await update.message.reply_text(
                    "✅ Documento aggiunto al database delle conoscenze!"
                )
                self.log_success(f"Document added: {file_path}")
            else:
                await update.message.reply_text(
                    "❌ Errore nel processare il documento."
                )
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            self.log_error(f"Error processing PDF: {e}", e)
            await update.message.reply_text(
                "❌ Errore nel caricare il documento."
            )
    
    def setup_handlers(self, application: Application) -> None:
        """Setup command and message handlers"""
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("info", self.info_command))
        application.add_handler(CommandHandler("resources", self.resources_command))
        application.add_handler(CommandHandler("usage", self.usage_command))
        application.add_handler(CommandHandler("addknowledge", self.addknowledge_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        application.add_handler(
            MessageHandler(filters.Document.PDF, self.handle_document)
        )
        self.log_success("Telegram handlers configured")
    
    async def setup_bot_commands(self, application: Application) -> None:
        """Setup bot command menu visible in Telegram UI"""
        commands = [
            BotCommand("start", "🏠 Avvia il bot e mostra il messaggio di benvenuto"),
            BotCommand("help", "❓ Mostra l'elenco dei comandi disponibili"),
            BotCommand("stats", "📊 Visualizza statistiche del bot"),
            BotCommand("info", "ℹ️ Informazioni sul bot"),
            BotCommand("resources", "🔗 Link alle dashboard dei servizi"),
            BotCommand("usage", "📈 Utilizzo in tempo reale dei servizi"),
            BotCommand("addknowledge", "📚 Aggiungi conoscenza alla base dati"),
        ]
        
        try:
            await application.bot.set_my_commands(commands)
            self.log_success("Bot commands menu configured")
        except Exception as e:
            self.log_error(f"Failed to setup bot commands menu: {e}", e)
    
    def run(self) -> None:
        """Start the Telegram bot"""
        token = os.getenv(self.config.token_env)
        
        if not token:
            self.log_error(f"Missing {self.config.token_env} environment variable")
            raise ValueError(f"Missing {self.config.token_env} environment variable")
        
        # Create application
        self.application = Application.builder().token(token).build()
        
        # Setup handlers
        self.setup_handlers(self.application)
        
        # Setup bot commands menu (async operation)
        self.application.post_init = self.setup_bot_commands
        
        # Start bot
        self.log_info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
