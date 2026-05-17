import uuid
from langchain_core.tools import tool
from langchain_chroma import Chroma
# Cambiamos la importación para usar el ecosistema de Ollama local
from langchain_ollama import OllamaEmbeddings 

# Inicializar los embeddings usando tu modelo local de Ollama
# Asegúrate de que Ollama esté corriendo en tu máquina ('ollama serve')
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest"
)

# Configurar/Conectar a la base de datos persistente de Chroma
# Creamos o abrimos la colección 'python_knowledge'
vector_store = Chroma(
    collection_name="python_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"  # Se guardará localmente en esta carpeta
)

@tool
def index_python_chunk(content: str, category: str = "general") -> str:
    """
    Indexa un fragmento (chunk) de código o documentación de Python en el banco de conocimiento.
    Usa esta herramienta cuando descubras o generes información valiosa sobre Python que deba recordarse.
    """
    try:
        # Generar un ID único para el documento
        doc_id = str(uuid.uuid4())
        
        # Estructurar los metadatos para optimizar filtros semánticos futuros
        metadata = {"category": category, "source": "agent_generation"}
        
        # Añadir al almacén de vectores
        vector_store.add_texts(
            texts=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return f"Éxito: Chunk indexado correctamente en el banco 'Python' con ID: {doc_id} usando Qwen3-Embedding."
    except Exception as e:
        return f"Error al indexar en Chroma: {str(e)}"

@tool
def retrieve_python_knowledge(query: str, category: str = None) -> str:
    """
    Busca de manera semántica información, soluciones, payloads o documentación sobre Python 
    dentro del banco de conocimiento. Retorna los fragmentos más relevantes.
    """
    try:
        # Configurar filtro opcional por categoría si el agente lo deduce
        search_filter = {"category": category} if category else None
        
        # Realizar la búsqueda por similitud (k=3 fragmentos relevantes)
        results = vector_store.similarity_search(query, k=3, filter=search_filter)
        
        if not results:
            return "No se encontró información relevante en el banco de conocimiento de Python."
        
        # Formatear la salida para el agente
        formatted_results = []
        for i, doc in enumerate(results, 1):
            formatted_results.append(f"--- Resultado {i} (Categoría: {doc.metadata.get('category')}) ---\n{doc.page_content}\n")
            
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Error al realizar el retrieval en Chroma: {str(e)}"