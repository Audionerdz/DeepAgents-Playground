# mainpy guide (PoC AI Engineering)

# 🧪 The Frankenstein Lab Manifesto: PoC AI Engineering

Para construir agentes que funcionen, primero hay que entender que un **Proof of Concept (PoC)** no es una catedral; es un laboratorio lleno de cables y notas adhesivas. La prioridad es la **validación**, no la perfección.

---

## 🎯 Objetivos de un PoC
Antes de escalar, el sistema debe responder con éxito a:
* **Velocidad de experimentación:** ¿Qué tan rápido puedo probar una idea nueva?
* **Descubrimiento de límites:** ¿Dónde se rompe el razonamiento del modelo?
* **Validación de Tools:** ¿El modelo entiende cuándo y cómo llamar a la función?
* **UX de Orchestration:** ¿La delegación entre sub-agentes es fluida o redundante?

---

## 🛠️ Por qué el "Monolito Experimental" Funciona
1. **Visibilidad Total:** Todo (prompts, tools, backend) está a la vista. Menos saltos entre archivos = más velocidad mental.
2. **Debugging Quírúrgico:** Si algo falla, sabes exactamente qué tool explotó sin hacer "arqueología espacial" en capas de abstracción.
3. **Modularidad Orgánica:** La estructura nace del uso real, no de una teoría de diseño impuesta.
