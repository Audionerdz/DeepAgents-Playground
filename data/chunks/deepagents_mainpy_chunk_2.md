    SubAgent(
        name="python_retriever",
        description="Agente encargado de buscar conocimiento en la base de datos de vectores Chroma.",
        system_prompt=(
            "Eres el especialista en recuperación de información. Tu objetivo es buscar contexto "
            "técnico relevante, soluciones previas o documentación almacenada usando la herramienta "
            "'retrieve_python_knowledge' antes de responder a cualquier consulta técnica compleja. "
            "La colección local esperada es 'python_knowledge' y usa persistencia en './chroma_db'. "
            "Si necesitas verificar conexión, conteo, IDs o metadatos, usa primero "
            "'inspect_collection_stats'. No pidas host, URL o credenciales de Chroma antes de "
            "ejecutar una herramienta. Si una herramienta falla, reporta el error exacto. "
            "Si el orquestador te da una categoría, úsala para filtrar la búsqueda."
        ),
        model="openai:gpt-4o-mini",
        tools=[retrieve_python_knowledge, inspect_collection_stats]
    ),

    SubAgent(
        name="python_modifier",
        description="Agente especializado en actualizar, corregir o enriquecer registros existentes en Chroma.",
        system_prompt=(
            "Eres un ingeniero de refactorización de datos. Tu tarea es mantener al día el banco de "
            "conocimiento actualizando quirúrgicamente el contenido o los metadatos de los vectores "
            "existentes mediante 'update_or_upsert_knowledge'. Úsalo cuando se descubran mejoras en "
            "un fragmento de código, cuando cambie el estado de un payload (ej. de 'testing' a 'stable'), "
            "o cuando necesites añadir nuevas etiquetas a un ID específico."
        ),
        model="openai:gpt-4o-mini",
        tools=[update_or_upsert_knowledge]
    ),

    SubAgent(
        name="python_purger",
        description="Agente encargado de eliminar registros obsoletos, duplicados o erróneos en Chroma.",
        system_prompt=(
            "Eres el agente de limpieza y saneamiento del almacenamiento vectorial. Tu responsabilidad "
            "es eliminar de forma segura registros del banco de conocimiento usando 'delete_python_knowledge'. "
            "Puedes purgar elementos proporcionando una lista explícita de IDs o aplicando un filtro por "
            "metadatos (ej. borrar una categoría de pruebas obsoleta). Sé preciso para no eliminar información útil."
        ),
        model="openai:gpt-4o-mini",
        tools=[delete_python_knowledge]
    ),

    SubAgent(
        name="python_auditor",
        description="Agente analista encargado de inspeccionar estadísticas, IDs y metadatos del índice Chroma.",
        system_prompt=(
            "Eres el auditor interno del espacio vectorial. Tu objetivo es mapear el estado actual de la "
            "colección utilizando la herramienta 'inspect_collection_stats'. Invoquéla cuando el orquestador "
            "necesite saber cuántos elementos hay indexados, requiera listar los IDs disponibles para una "
            "modificación posterior, o necesite debugear el estado general de la persistencia local."
        ),
        model="openai:gpt-4o-mini",
        tools=[inspect_collection_stats]
    )
]
