## 📈 Roadmap de Evolución de un Agente

| Fase | Enfoque | Componentes Clave |
| :--- | :--- | :--- |
| **Fase 1** | El Script | `agent.py` (Todo en uno) |
| **Fase 2** | Desacoplamiento | `/tools`, `/prompts` |
| **Fase 3** | Especialización | `/subagents`, `/orchestrator` |
| **Fase 4** | Persistencia | PostgreSQL, Vector DB, Redis |
| **Fase 5** | Interfaz | CopilotKit, Streamlit, Next.js |
| **Fase 6** | Producción | Docker, Async Workers, Tracing (LangSmith) |

---

## 🚫 Lo que NO debes hacer (Incluso en PoCs)
* **Giant Prompts:** No metas 9000 líneas en un solo prompt. **Divide y vencerás.**
* **Tools Ambiguas:** Evita funciones como `do_everything()`. Usa herramientas granulares como `read_file()` o `execute_sql()`. 
* **Sub-agentes sin Identidad:** Cada agente debe ser como un NPC técnico en un RPG cyberpunk: con rol, límites y especialidad clara. 🕶️
