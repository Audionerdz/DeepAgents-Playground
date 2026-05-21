#mainpy #compositebackend #base #fase1 

Nota indexable (fragmento desde /deepagents/mainpy.md.md):

```python
# /// script
# requires-python = ">=3.12"

# Importaciones de LangChain y LangGraph
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# Importaciones específicas y nativas de DeepAgents
from deepagents import create_deep_agent
from deepagents.middleware.subagents import SubAgent
from deepagents.backends import FilesystemBackend, StoreBackend, StateBackend, CompositeBackend

from copilotkit import CopilotKitMiddleware

# Configuración de almacenamiento
# Path("data/memories").mkdir(parents=True, exist_ok=True)
# Path("data/chunks").mkdir(parents=True, exist_ok=True)
# Path("data/deepagents").mkdir(parents=True, exist_ok=True)

# Memorias persistentes (FilesystemBackend)
# memories_backend = FilesystemBackend(root_dir="data/memories", virtual_mode=True)
# chunks_backend = FilesystemBackend(root_dir="data/chunks", virtual_mode=True)
# deepagents_backend = FilesystemBackend(root_dir="data/deepagents", virtual_mode=True)

# CompositeBackend con rutas:
# composite_backend = CompositeBackend(
#    default=StateBackend(),
#    routes={"/memories/": memories_backend, "/chunks/": chunks_backend, "/deepagents/": deepagents_backend}
# )

# Orquestación multi-agente: definición de subagentes
# - python_indexer: indexa fragmentos en ChromaDB usando index_python_chunk
# - python_retriever: recupera conocimiento usando retrieve_python_knowledge e inspect_collection_stats
# - python_modifier: actualiza/upserta usando update_or_upsert_knowledge
# - python_purger: elimina usando delete_python_knowledge
# - python_auditor: inspecciona stats/IDs usando inspect_collection_stats

# ORCHESTRATOR_SYSTEM_PROMPT incluye reglas estrictas para:
# - Antes de indexar en ChromaDB, guardar el texto en /chunks/
# - Persistir memoria en /memories/
# - Mantener configuración/estado de agentes en /deepagents/

# Runtime:
# agent = create_deep_agent(
#    model="openai:gpt-4o",
#    backend=composite_backend,
#    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
#    tools=[retrieve_python_knowledge, inspect_collection_stats],
#    middleware=[CopilotKitMiddleware()],
#    subagents=subagents,
# )

# if __name__ == "__main__": valida OPENAI_API_KEY y arranca.
```
