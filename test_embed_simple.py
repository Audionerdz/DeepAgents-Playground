import time, os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

t0 = time.time()
print("1. Importando...")
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
print(f"   OK ({time.time()-t0:.1f}s)")

t0 = time.time()
print("2. Creando OllamaEmbeddings...")
embeddings = OllamaEmbeddings(model="qwen3-embedding:latest", base_url="http://localhost:11434")
print(f"   OK ({time.time()-t0:.1f}s)")

t0 = time.time()
print("3. Probando embed_query...")
r = embeddings.embed_query("hola")
print(f"   Dims={len(r)} ({time.time()-t0:.1f}s)")

t0 = time.time()
print("4. Cargando Chroma...")
store = Chroma(
    collection_name="python_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
print(f"   OK ({time.time()-t0:.1f}s)")

t0 = time.time()
print("5. Contando vectores...")
total = store._collection.count()
print(f"   Total: {total} ({time.time()-t0:.1f}s)")

t0 = time.time()
print("6. similarity_search...")
results = store.similarity_search("Python", k=3)
print(f"   Resultados: {len(results)} ({time.time()-t0:.1f}s)")

for i, doc in enumerate(results, 1):
    print(f"\n--- Resultado {i} ---")
    print(f"  Categoría: {doc.metadata.get('category')}")
    print(f"  Contenido: {doc.page_content[:200]}")

print("\n=== TODO OK ===")
