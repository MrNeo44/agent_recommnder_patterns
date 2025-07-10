import os
import asyncio
import threading
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agent.bdi_agent import BDIRecommenderAgent

load_dotenv()
app = Flask(__name__)

# Colas asíncronas para comunicar con el agente
input_queue = asyncio.Queue()
output_queue = asyncio.Queue()

# Crear instancia del agente
agent_jid = os.getenv("BDI_AGENT_JID")
agent_pass = os.getenv("BDI_AGENT_PASSWORD")
agent = BDIRecommenderAgent(agent_jid, agent_pass, input_queue, output_queue)

# Iniciar el agente de forma asíncrona en segundo plano
async def start_agent():
    await agent.start(auto_register=True)

def agent_loop():
    asyncio.run(start_agent())

threading.Thread(target=agent_loop, daemon=True).start()

@app.route("/analyze", methods=["POST"])
async def analyze():
    data = request.get_json()
    code = data.get("code", "")
    print(f"Código recibido en la API: {code}")

    # Poner el código en la cola de entrada
    await input_queue.put(code)
    print("Código agregado a la cola de entrada.")

    try:
        # Esperar el patrón de la cola con un timeout
        pattern = await asyncio.wait_for(output_queue.get(), timeout=3600)  # Aumenta el timeout si es necesario
        print("Patrón recibido de la cola:", pattern)
        return jsonify({"pattern": pattern})
    except asyncio.TimeoutError:
        print("Timeout esperando el patrón.")
        return jsonify({"error": "Tiempo de espera agotado para encontrar el patrón."}), 504


if __name__ == "__main__":
    port = int(os.getenv("BRIDGE_PORT", 5000))
    print(f"Iniciando REST API en http://localhost:{port}")
    app.run(port=port)
