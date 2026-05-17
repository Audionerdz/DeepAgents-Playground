"""
Módulo de inicialización para las herramientas agénticas de Chroma DB.
Inicializa el almacenamiento vectorial local usando Ollama Embeddings.
"""

from .tools import (
    embeddings,
    vector_store,
    index_python_chunk,
    retrieve_python_knowledge
)

# Definimos qué componentes se exportan limpiamente cuando se importe el módulo
__all__ = [
    "embeddings",
    "vector_store",
    "index_python_chunk",
    "retrieve_python_knowledge"
]