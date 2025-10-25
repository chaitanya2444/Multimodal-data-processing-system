np
FAISS_INDEX_FILE = os.environ.get('FAISS_INDEX_FILE', 'faiss.index')




def init_db():
conn = sqlite3.connect(DB)
conn.execute("""CREATE TABLE IF NOT EXISTS docs(
id TEXT PRIMARY KEY, source TEXT, text TEXT, chunk_index INT)
""")
conn.commit()
conn.close()




class VectorStore:
def __init__(self, dim: int):
self.dim = dim
self.index = faiss.IndexFlatL2(dim)
self.ids = []


def add(self, vecs, metadatas):
arr = np.array(vecs).astype('float32')
self.index.add(arr)
self.ids.extend(metadatas)


def search(self, qvec, k=5):
q = np.array([qvec]).astype('float32')
D, I = self.index.search(q, k)
results = []
for idx in I[0]:
if idx == -1:
continue
results.append(self.ids[idx])
return results


def save(self, path=FAISS_INDEX_FILE):
faiss.write_index(self.index, path)


def load(self, path=FAISS_INDEX_FILE):
if os.path.exists(path):
self.index = faiss.read_index(path)




# helpers for sqlite metadata


def save_doc(id: str, source: str, text: str, chunk_index: int):
conn = sqlite3.connect(DB)
conn.execute("INSERT OR REPLACE INTO docs(id, source, text, chunk_index) VALUES (?,?,?,?)",
(id, source, text, chunk_index))
conn.commit()
conn.close()




def get_doc_text(id: str) -> str:
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT text FROM docs WHERE id=?", (id,))
r = cur.fetchone()
conn.close()
return r[0] if r else ""
