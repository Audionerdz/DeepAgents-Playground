## 📂 Estructura de Proyecto Sugerida (Minimalista)

```text
project/
├── agent.py         # Lógica central y orquestación
├── tools.py         # Definición de funciones/herramientas
├── prompts.py       # System strings y templates
├── workspace/       # Filesystem local para el agente
└── requirements.txt # Dependencias (LangGraph, DeepAgents, etc.)
```

> **Regla de Oro:** Aprendes más construyendo 20 mini-agentes "descartables" y agresivamente experimentales que intentando diseñar la arquitectura definitiva desde el día uno. **¡Rompe cosas rápido!** 👾
