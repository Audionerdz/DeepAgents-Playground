#mainpy #compositebackend #base #fase1 

```python
# /// script

# requires-python = ">=3.12"

# dependencies = [

#     "deepagents",

#     "langchain",

#     "langchain-openai",

# ]

# ///

#!/usr/bin/env python3

import os

import sys

from pathlib import Path

# Importaciones de LangChain y LangGraph
from langchain_core.tools import tool

from langgraph.checkpoint.memory import MemorySaver

# Importaciones específicas y nativas de DeepAgents
from deepagents import create_deep_agent

from deepagents.middleware.subagents import SubAgent

from deepagents.backends import FilesystemBackend, StoreBackend, StateBackend, CompositeBackend

from copilotkit import CopilotKitMiddleware

# 0. CONFIGURACIÓN DE HERRAMIENTAS (CHROMA)
from chroma_tools import (
    index_python_chunk,
    retrieve_python_knowledge,
    delete_python_knowledge,
    update_or_upsert_knowledge,
    inspect_collection_stats
)

# CONFIGURACIÓN DE STORAGE Y DIRECTORIOS
Path("data/memories").mkdir(parents=True, exist_ok=True)
Path("data/chunks").mkdir(parents=True, exist_ok=True)
Path("data/deepagents").mkdir(parents=True, exist_ok=True)

memories_backend = FilesystemBackend(
    root_dir="data/memories",
    virtual_mode=True
)

chunks_backend = FilesystemBackend(
    root_dir="data/chunks",
    virtual_mode=True
)

# deepagents_backend
 deepagents_backend = FilesystemBackend(
    root_dir="data/deepagents",
    virtual_mode=True
)

# Crear CompositeBackend con las 3 rutas
composite_backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/memories/": memories_backend,
        "/chunks/": chunks_backend,
        "/deepagents/": deepagents_backend,
    }
)

# 1. CONTEXTO Y CONFIGURACIÓN DE SUBAGENTES
subagents = [
    SubAgent(
        name="python_indexer",
        description="Agente encargado de indexar fragmentos de código en Chroma.",
        system_prompt=(
            "Eres un indexador técnico experto. Tu única tarea es estructurar, formatear e "
            "indexar fragmentos de código, payloads o documentación valiosa de Python en "
            "Chroma usando la herramienta 'index_python_chunk'. Clasifica siempre el contenido "
            "en categorías lógicas (ej. 'exploits', 'network', 'decorators', 'async') para "
            "optimizar búsquedas futuras."
        ),
        model="openai:gpt-4o-mini",
        tools=[index_python_chunk]
    ),
