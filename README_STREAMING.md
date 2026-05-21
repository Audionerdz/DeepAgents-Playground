# Estudio de Streaming con create_deep_agent

## Estructura del Proyecto

```
main_stream_study.py          <- Backend Python simplificado
frontend_example/
  App.tsx                     <- Componente React para consumir el stream
README_STREAMING.md           <- Esta guia
```

## Como Funciona el Streaming

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (Python)                        │
│                                                             │
│  create_deep_agent                                          │
│    ├── model: openai:gpt-4o-mini                           │
│    ├── tools: [get_weather, calcular]                      │
│    ├── backend: FilesystemBackend                          │
│    └── middleware: [CopilotKitMiddleware()]  ◄── CLAVE     │
│                                                             │
│  El middleware expone un HTTP server en localhost:2024     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ SSE / HTTP Stream
                               │ (token por token)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│                                                             │
│  useStream<AgentState>({                                    │
│    apiUrl: "http://localhost:2024",                        │
│    assistantId: "agent"                                    │
│  })                                                         │
│                                                             │
│  stream.messages  ← array reactivo que crece con tokens    │
│  stream.toolCalls ← tool calls en tiempo real              │
│  stream.isLoading ← estado del stream                      │
│  stream.submit()  ← envia mensajes al agente               │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Streaming Token por Token

1. **Usuario envia mensaje** → `stream.submit({ messages: [new HumanMessage("Que clima hace en Madrid?")] })`

2. **Backend procesa** → `create_deep_agent` recibe el mensaje y el LLM comienza a generar tokens

3. **Tokens llegan uno a uno** → El `CopilotKitMiddleware` envia cada token via SSE (Server-Sent Events)

4. **Frontend acumula** → `useStream` acumula los tokens en `msg.text` de forma reactiva

5. **UI se actualiza** → React re-renderiza el componente con el nuevo texto acumulado

6. **Tool calls** → Si el agente decide usar una herramienta, `stream.toolCalls` se actualiza con el nombre, args y resultado

## Diferencias: create_agent vs create_deep_agent

| Aspecto | create_agent | create_deep_agent |
|---------|-------------|-------------------|
| Paquete | `langchain` | `deepagents` |
| Backend | checkpointer simple | CompositeBackend con rutas |
| Herramientas | tools directas | tools + subagents + filesystem |
| Middleware | compatible | compatible (CopilotKitMiddleware) |
| Streaming | igual | igual (mismo protocolo) |

**Para streaming al frontend, ambos funcionan igual.** El middleware es lo que importa.

## Como Correr

### 1. Backend Python

```bash
# Variables de entorno
export OPENAI_API_KEY="tu-api-key"

# Correr el agente
python main_stream_study.py
```

### 2. Frontend React

```bash
# Crear proyecto
npm create vite@latest frontend -- --template react-ts
cd frontend

# Instalar dependencias
npm install @langchain/react @langchain/core react-markdown remark-gfm

# Reemplazar src/App.tsx con el contenido de frontend_example/App.tsx

# Correr
npm run dev
```

### 3. Conectar Backend y Frontend

El `CopilotKitMiddleware` expone automaticamente el agente. Para desarrollo local, necesitas un servidor que haga de puente. Las opciones son:

**Opcion A: copilotkit CLI**
```bash
pip install copilotkit
copilotkit dev --port 2024
```

**Opcion B: langgraph-server**
```bash
pip install langgraph-cli
langgraph up --port 2024
```

## Que Observar en el Streaming

### 1. Tokens llegando en tiempo real
- Abre el console del navegador
- Mira como `stream.messages[messages.length-1].text` crece caracter por caracter
- El `ReactMarkdown` re-renderiza con cada nuevo token

### 2. Tool calls apareciendo
- Cuando preguntas "Que clima hace en Madrid?", veras:
  1. Primero el tool call aparece con `name: "get_weather"` y `args: { city: "Madrid" }`
  2. Luego aparece el `output` con el resultado
  3. Finalmente el AI genera su respuesta usando ese resultado

### 3. Estado isLoading
- `stream.isLoading` es `true` mientras el agente esta pensando/generando
- Se pone `false` cuando termina

## Ejemplos de Prompts para Probar

```
1. "Hola, como estas?"                    -> Respuesta directa, streaming simple
2. "Que clima hace en Madrid?"            -> Tool call: get_weather
3. "Calcula 15 * 23"                      -> Tool call: calcular
4. "Que clima hace en Tokio y en Paris?"  -> Multiple tool calls
5. "Explica que herramientas tienes"      -> Respuesta conversacional
```

## Troubleshooting

### Error: "No se pudo conectar a localhost:2024"
- Verifica que el servidor del agente este corriendo
- Revisa que el puerto sea correcto en `AGENT_URL`

### Los tokens no aparecen en tiempo real
- Verifica que `CopilotKitMiddleware()` este en la lista de middleware
- Revisa la consola del navegador por errores de CORS

### Tool calls no se muestran
- Verifica que las herramientas esten registradas en `create_deep_agent`
- Revisa que `stream.toolCalls` no este vacio en React DevTools
