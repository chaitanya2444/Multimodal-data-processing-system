import os
import google.generativeai as genai


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
raise EnvironmentError("Please set GEMINI_API_KEY in your environment")


genai.configure(api_key=GEMINI_API_KEY)




def embed_text(text: str):
"""Return embedding vector for `text` using Gemini embedding model."""
# Keep inputs reasonably sized (chunking handled by ingest)
res = genai.embeddings.create(model="gemini-embedding-001", input=text)
# SDK returns object with data[0].embedding
return res.data[0].embedding
