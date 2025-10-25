import os
elif ext in ['.png', '.jpg', '.jpeg']:
text = image_processor.ocr_image(p)
elif ext in ['.mp3', '.wav']:
text = audio_processor.transcribe_audio(p)
elif ext in ['.mp4', '.mkv']:
# naive: extract audio externally using ffmpeg and then transcribe
audio_out = p + '.mp3'
from app.processors.video_processor import extract_audio_from_video
extract_audio_from_video(p, audio_out)
text = audio_processor.transcribe_audio(audio_out)
else:
print(f"Skipping unsupported file: {p}")
return


if not text or text.strip() == "":
print(f"No text extracted from {p}")
return


chunks = chunk_text(text)
vecs = []
metadatas = []
for i, c in enumerate(chunks):
emb = embed_text(c)
vid = str(uuid4())
vecs.append(emb)
metadatas.append(vid)
retriever.save_doc(vid, p, c, i)


vectorstore.add(vecs, metadatas)




def ingest_folder(folder: str):
retriever.init_db()
# create vectorstore with a guessed dim (user may override VECTOR_DIM env)
dim = int(os.environ.get('VECTOR_DIM', 1536))
vs = retriever.VectorStore(dim=dim)


p = Path(folder)
files = list(p.rglob('*'))
for f in tqdm(files):
if f.is_file():
try:
process_file(f, vs)
except Exception as e:
print(f"Error processing {f}: {e}")


# save faiss index to disk
vs.save()
print("Ingestion complete. FAISS index saved.")




if __name__ == '__main__':
if len(sys.argv) < 2:
print("Usage: python app/ingest.py <folder_with_data>")
sys.exit(1)
ingest_folder(sys.argv[1])
