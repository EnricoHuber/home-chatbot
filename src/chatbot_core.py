# chatbot_core.py - versione "v1" (senza RAG)
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class HomeChatbot:
    def __init__(self):
        """Inizializza solo il modello LLM"""
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    async def get_response(self, user_message: str, user_id: int) -> str:
        """Invia il messaggio all'LLM e restituisce la risposta"""
        prompt = f"""Sei un assistente domestico amichevole e utile.
Rispondi alla seguente domanda in modo naturale e pratico:

Utente: {user_message}
"""

        try:
            response = await self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ Errore durante la risposta: {str(e)[:100]}"
