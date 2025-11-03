"""Quick test to verify Supabase connection"""
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "None")

try:
    from supabase import create_client, Client
    print(f"\n✅ Supabase package imported successfully")
    
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"✅ Supabase client created successfully")
    
    # Test connection by querying the knowledge_base table
    result = client.table("knowledge_base").select("id").limit(1).execute()
    print(f"✅ Supabase connection successful!")
    print(f"Query result: {result}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
