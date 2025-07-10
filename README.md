# Agente Proactivo BDI-LLM para Recomendación de Patrones de Diseño

Este proyecto implementa un agente inteligente basado en la arquitectura BDI (Belief–Desire–Intention), con capacidades de aprendizaje adaptativo gracias a su integración con un modelo LLM (GPT-4o). Funciona de forma proactiva en Visual Studio Code, detectando automáticamente *code smells* al guardar archivos y recomendando patrones de diseño apropiados, incluso aprendiendo nuevas reglas a partir de interacciones con el LLM.

## Estructura del Proyecto

## 📁 Estructura del Proyecto
A continuación se detalla la estructura del proyecto, que incluye tanto la lógica del agente como la extensión:

```text
agent_recommender_patterns/
├── agent/                      # Lógica del agente inteligente
│   ├── bdi_agent.py            # Agente SPADE con razonamiento BDI + aprendizaje desde el LLM
│   └── knowledge_base.json     # Base de conocimiento autoadaptativa y persistente
│
├── extension/                  # Extensión para Visual Studio Code (TypeScript)
│   └── ...                     # Archivos fuente (ver README específico en esta carpeta)
│
├── bridge_server.py            # Servidor HTTP que comunica VS Code con el agente
├── sample_code.py              # Código Python de prueba con múltiples code smells
├── .env                        # Variables sensibles (API keys, credenciales XMPP, etc.)
└── README.md                   # Documentación principal del proyecto
```

## Requisitos

- Python 3.12
- Node.js 24 (para compilar la extensión)
- Visual Studio Code
- Cuenta en [OpenAI Platform](https://platform.openai.com/)
- Servidor HTTP para la comunicación entre VS Code y el agente (puede ser local o remoto)


## Configuración `.env`

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
BDI_JID=agent@localhost
BDI_PASSWORD=123456
XMPP_SERVER=localhost
BRIDGE_PORT=5000
```

### Instrucciones de instalación

Seguir los siguientes pasos: 

#### 1. Clonar el repositorio

```bash
git clone https://github.com/MrNeo44/agent_recommnder_patterns.git
cd agent_recommnder_patterns
```

#### 2. Crear y configurar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 3. Instalar dependencias del backend 
```bash
pip install -r requirements.txt
```
#### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
OPENAI_API_KEY=sk-...             # Tu API key de OpenAI
BDI_AGENT_JID=agent@jabber.org    # JID del agente SPADE
BDI_AGENT_PASSWORD=tu_contraseña
BDI_AGENT_HOST=localhost
BDI_AGENT_PORT=5222
```

#### 5. Ejecutar el server

Este componente escucha peticiones desde la extensión de VS Code:

```bash
python bridge_server.py
```

#### 6. Iniciar el agente BDI

En otra terminal:

```bash
python agent/bdi_agent.py
```

#### 7. Instalar y configurar la extensión de VS Code

```bash
cd extension/
npm install        # Instala las dependencias
npm run compile    # Compila TypeScript a JavaScript
```

Luego, abre la carpeta `extension/` en Visual Studio Code y presiona `F5` para lanzar la extensión en modo desarrollo.

---

**Nota** Cada vez que guardes un archivo `.py`, será enviado automáticamente al agente para su análisis y recomendación.