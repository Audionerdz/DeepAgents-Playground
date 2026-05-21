import os, shutil, time
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "qwen3-embedding:latest")

t0 = time.time()
print("1. Inicializando OllamaEmbeddings...")
embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_BASE_URL)

# Verificar dims de la query
test_embed = embeddings.embed_query("test")
print(f"   Dims: {len(test_embed)} ({time.time()-t0:.1f}s)")

# Ver si la colección existente tiene dims compatibles
COLLECTION = "python_knowledge"
PERSIST_DIR = "./chroma_db"

store = Chroma(
    collection_name=COLLECTION,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)
existing_total = store._collection.count()

if existing_total > 0:
    # Chequear dims de un vector existente
    sample = store._collection.get(limit=1)
    existing_dims = len(sample["embeddings"][0]) if sample.get("embeddings") else None
    if existing_dims and existing_dims != len(test_embed):
        print(f"\n2. ¡Dimensiones incompatibles!")
        print(f"   Colección existente: {existing_dims} dims")
        print(f"   Nuevo embedding: {len(test_embed)} dims")
        print("   Borrando chroma_db para recrear...")
        store._collection.delete(where={})
        del store
        # Borrar la base de datos persistente
        if os.path.exists(PERSIST_DIR):
            shutil.rmtree(PERSIST_DIR)
        print("   OK. Recreando colección...")
        store = Chroma(
            collection_name=COLLECTION,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )
        existing_total = 0
    else:
        print(f"\n2. Dimensiones compatibles: {existing_dims} dims")
else:
    print(f"\n2. Colección vacía, lista para indexar.")

print(f"\n3. Total de vectores: {existing_total}")

print("\n4. Indexando documento de prueba...")
t0 = time.time()
store.add_texts(
    texts=[
        "Python es un lenguaje de programación interpretado, dinámico y multiplataforma. Fue creado por Guido van Rossum.",
        "LangChain es un framework para construir aplicaciones con LLMs. Permite crear cadenas, agentes y RAG.",
        "Ollama permite ejecutar modelos de lenguaje localmente, como qwen, gemma, llama y muchos más.",
    ],
    metadatas=[
        {"category": "general", "source": "test"},
        {"category": "frameworks", "source": "test"},
        {"category": "tools", "source": "test"},
    ],
    ids=["doc_python", "doc_langchain", "doc_ollama"],
)
print(f"   3 documentos indexados ({time.time()-t0:.1f}s)")
print(f"   Total ahora: {store._collection.count()}")

print("\n5. Buscando 'lenguaje de programación'...")
t0 = time.time()
results = store.similarity_search("lenguaje de programación", k=3)
print(f"   Encontrados: {len(results)} ({time.time()-t0:.1f}s)")

for i, doc in enumerate(results, 1):
    meta = doc.metadata or {}
    print(f"\n--- Resultado {i} ---")
    print(f"  Categoría: {meta.get('category')}")
    print(f"  Contenido: {doc.page_content[:200]}")

print("\n6. Buscando 'framework para LLMs'...")
t0 = time.time()
results = store.similarity_search("framework para LLMs", k=3)
print(f"   Encontrados: {len(results)} ({time.time()-t0:.1f}s)")

for i, doc in enumerate(results, 1):
    meta = doc.metadata or {}
    print(f"\n--- Resultado {i} ---")
    print(f"  Categoría: {meta.get('category')}")
    print(f"  Contenido: {doc.page_content[:200]}")

print("\n=== TODO OK ===")
