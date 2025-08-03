# Raingear

Prueba tecninca analista de datos

Este proyecto aborda un caso de estudio para una empresa minorista de ropa para lluvia que busca predecir ventas futuras y analizar tendencias de productos. Se ha implementado un flujo de datos que incluye ETL, almacenamiento en PostgreSQL (simulando una base de datos local o externa) y Supabase (para respaldo y posible despliegue), y un tablero interactivo en Looker Studio.

1.  **Revisar imagenes en src\assets:**
    diagrama db
    dashboard:https://lookerstudio.google.com/reporting/cae6ae50-cdbb-414c-ab54-ff713a29282d
1.  **Clonar el repositorio:**

1.  **Crear y activar un entorno virtual (recomendado):**
    python -m venv venv

1.  **Instalar dependencias:**
    pip install -r requirements.txt

1.  **Crear .env con las siguientes variables:**
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    DB_NAME=

    SUPABASE_URL=
    SUPABASE_SERVICE_KEY=
    SUPABASE_TABLE=
