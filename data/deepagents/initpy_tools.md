#architecture #tips #init 

```text id="e0n1j6"
myproject/
│
├── main.py
│
└── src/
    ├── __init__.py
    │
    ├── agents/
    │   ├── __init__.py
    │   ├── pentester.py
    │   ├── researcher.py
    │   └── osint.py
    │
    └── tools/
        ├── __init__.py
        ├── web.py
        ├── network.py
        ├── system.py
        └── osint.py
```

---

# 📦 `src/tools/__init__.py`

Este centraliza TODAS las herramientas.

```python id="n90db4"
# src/tools/__init__.py

"""
Registry global de herramientas del sistema.
"""

# =========================
# WEB TOOLS
# =========================

from .web import (
    search_tool,
    scraper_tool,
)

# =========================
# NETWORK TOOLS
# =========================

from .network import (
    nmap_tool,
    dns_tool,
)

# =========================
# SYSTEM TOOLS
# =========================

from .system import (
    read_file_tool,
)

# =========================
# OSINT TOOLS
# =========================

from .osint import (
    whois_tool,
    email_lookup_tool,
)

# =========================
# TOOL GROUPS
# =========================

WEB_TOOLS = [
    search_tool,
    scraper_tool,
]

NETWORK_TOOLS = [
    nmap_tool,
    dns_tool,
]

SYSTEM_TOOLS = [
    read_file_tool,
]

OSINT_TOOLS = [
    whois_tool,
    email_lookup_tool,
]

# Arsenal completo
ALL_TOOLS = (
    WEB_TOOLS
    + NETWORK_TOOLS
    + SYSTEM_TOOLS
    + OSINT_TOOLS
)

# =========================
# PUBLIC EXPORTS
# =========================

__all__ = [
    # Individual tools
    "search_tool",
    "scraper_tool",
    "nmap_tool",
    "dns_tool",
    "read_file_tool",
    "whois_tool",
    "email_lookup_tool",

    # Tool groups
    "WEB_TOOLS",
    "NETWORK_TOOLS",
    "SYSTEM_TOOLS",
    "OSINT_TOOLS",

    # Global registry
    "ALL_TOOLS",
]
```

---

# 🤖 `src/agents/__init__.py`

Este exporta TODOS los builders de agentes.

```python id="6dofp7"
# src/agents/__init__.py

"""
Registry global de agentes.
"""

from .pentester import build_pentester_agent
from .researcher import build_research_agent
from .osint import build_osint_agent

# =========================
# AGENT REGISTRY
# =========================

ALL_AGENTS = {
    "pentester": build_pentester_agent,
    "researcher": build_research_agent,
    "osint": build_osint_agent,
}

# =========================
# PUBLIC EXPORTS
# =========================

__all__ = [
    "build_pentester_agent",
    "build_research_agent",
    "build_osint_agent",
    "ALL_AGENTS",
]
```

---

# 🧠 Ejemplo de un agente

## `src/agents/pentester.py`

```python id="hpsxvv"
from src.tools import (
    NETWORK_TOOLS,
    SYSTEM_TOOLS,
)

def build_pentester_agent(model):

    tools = (
        NETWORK_TOOLS
        + SYSTEM_TOOLS
    )

    return {
        "name": "Pentester",
        "model": model,
        "tools": tools,
    }
```

---

# 🧠 Otro agente

## `src/agents/researcher.py`

```python id="x9q0u4"
from src.tools import (
    WEB_TOOLS,
)

def build_research_agent(model):

    return {
        "name": "Researcher",
        "model": model,
        "tools": WEB_TOOLS,
    }
```

---

# 🚀 `main.py`

Ahora el root queda absurdamente limpio.

```python id="m2jjlwm"
# main.py

from src.agents import ALL_AGENTS

def main():

    model = "gpt-5"

    pentester = ALL_AGENTS["pentester"](model)

    print(pentester)

if __name__ == "__main__":
    main()
```

---

# 🌌 Lo poderoso de esta arquitectura

Ya tienes:

```text id="4sxdy2"
src
├── tools       → capability layer
├── agents      → orchestration layer
└── main.py     → runtime entrypoint
```

Eso escala elegantemente hacia:
- multi-agent systems
- routing dinámico
- tool permissions
- plugin loading
- MCP servers
- GraphRAG
- DeepAgents
- LangGraph

---

# 🔥 Lo bonito del patrón

Desde cualquier parte del proyecto puedes hacer:

```python id="6f9v41"
from src.tools import ALL_TOOLS
```

o:

```python id="xj2r7y"
from src.agents import build_pentester_agent
```

sin importar dónde viven realmente los archivos.

Ese es el propósito real del `__init__.py`:
crear una API interna limpia para tu propio framework 🛰️