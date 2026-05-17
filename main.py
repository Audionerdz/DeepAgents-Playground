#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Importaciones de LangChain y LangGraph
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# Importaciones específicas y nativas de DeepAgents
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.subagents import SubAgent

# Middleware oficial de integración nativa
from copilotkit import CopilotKitMiddleware

# =====================================================================
# 0. CONFIGURACIÓN DE HERRAMIENTAS (CHROMA)
# =====================================================================
try:
    from chroma_tools.tools import index_python_chunk, retrieve_python_knowledge
except ImportError:
    @tool
    def index_python_chunk(chunk: str, metadata: dict = None) -> str:
        """Agente encargado de indexar fragmentos de código en Chroma."""
        return "Chunk indexado con éxito (Mock)."

    @tool
    def retrieve_python_knowledge(query: str) -> str:
        """Agente encargado de buscar conocimiento en Chroma."""
        return f"Resultado de búsqueda simulado."


# =====================================================================
# 1. CONTEXTO Y CONFIGURACIÓN DE SUBAGENTES
# =====================================================================
backend = FilesystemBackend(
    root_dir=str(Path.cwd()),
    virtual_mode=True
)

subagents = [
    SubAgent(
        name="python_indexer",
        description="Agente encargado de indexar fragmentos de código en Chroma.",
        system_prompt="Eres un indexador técnico. Formatea y guarda usando 'index_python_chunk'.",
        model="openai:gpt-4o-mini",
        tools=[index_python_chunk]
    ),
    SubAgent(
        name="python_retriever",
        description="Agente encargado de buscar conocimiento en Chroma.",
        system_prompt="Busca contexto técnico usando 'retrieve_python_knowledge' antes de responder.",
        model="openai:gpt-4o-mini",
        tools=[retrieve_python_knowledge]
    )
]

ORCHESTRATOR_SYSTEM_PROMPT = """Eres el Orquestador Central (Master Agent) de un entorno de desarrollo avanzado de Python.
Tu objetivo principal es coordinar la automatización de tareas, el análisis de código y la gestión de una base de datos de conocimiento persistente en Chroma.
Mantén un tono profesional, directo y enfocado en la eficiencia de código."""


# =====================================================================
# 2. DEFINICIÓN DEL AGENTE (CON MIDDLEWARE INTEGRADO)
# =====================================================================
# En DeepAgents, CopilotKitMiddleware mapea los estados y streams automáticamente.
agent = create_deep_agent(
    model="openai:gpt-4o-mini",
    backend=backend,
    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
    tools=[],
    middleware=[CopilotKitMiddleware()],  # <-- Integración nativa requerida por el quickstart
    subagents=subagents,
    
)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("[ERROR] Por favor define la variable de entorno OPENAI_API_KEY.", file=sys.stderr)
        sys.exit(1)

   

