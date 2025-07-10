import json, os, asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from agent.smell_detector import SmellDetector
from agent.rule_engine import RuleEngine
from agent.llm_interface import query_llm

# Ruta al archivo de regla
KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

queue_lock = asyncio.Lock()

# Funcion para cargar las reglas desde el archivo
def load_rules():
    try:
        with open(KB_PATH, 'r') as f:
            return json.load(f)  # Devuelve las reglas cargadas
    except FileNotFoundError:
        return []  # Si el archivo no se encuentra, devuelve una lista vacia

# Funcin para guardar las reglas en el archivo
def save_rules(rules):
    with open(KB_PATH, 'w') as f:
        json.dump(rules, f, indent=2)  # Guarda las reglas en formato JSON con una indentación de 2 espacios

class BDIRecommenderAgent(Agent):
    def __init__(self, jid, password, input_queue, output_queue):
        super().__init__(jid, password)
        self.input_queue = input_queue
        self.output_queue = output_queue

    class ReceiveCodeBehaviour(CyclicBehaviour):
        async def run(self):
            # Obtener el código desde la cola
            code = await self.agent.input_queue.get()

            # Detectar olores (smells)
            smells = self.agent.smell_detector.detect(code)
            print("Smells detectados:", smells)  # Verifica los smells detectados

            # Verificar si el patrón ya existe en las reglas
            pattern = self.agent.rule_engine.match(smells)
            print("Patrón encontrado:", pattern)

            # Si no se encuentra un patrón, consultar al LLM
            if not pattern:
                print('No existe un patrón para estos smells, consultando LLM...')
                pattern = query_llm(code, smells)  # Llamada al LLM para obtener un patrón
                print(f"Patrón devuelto por el LLM; {pattern}")

                # Si el LLM devuelve un patrón válido, lo añadimos a las reglas
                if pattern and pattern != "Error al obtener patrón":
                    self.agent.rules.append({"smells": smells, "pattern": pattern})
                    save_rules(self.agent.rules)  # Guarda las nuevas reglas en el archivo
                    print("Nueva regla aprendida:", pattern)
                else:
                    # Solo si el LLM no devuelve un patrón válido, asignamos el error
                    print("El LLM no devolvió un patrón válido.")
                    pattern = "Error al obtener patrón"

            else:
                print("Usando patrón existente:", pattern)

            # Agregar el patrón final a la cola de salida
            print("Agregando patrón final:", pattern)
            async with queue_lock:
                await self.agent.output_queue.put(pattern)

            # Marcar como completado
            self.agent.input_queue.task_done()

    async def setup(self):
        print(f"Agente BDI-LLM iniciado: {self.jid}")
        # Inicializar el detector de olores y el motor de reglas
        self.smell_detector = SmellDetector()
        self.rules = load_rules()
        self.rule_engine = RuleEngine(self.rules)  # Crear el motor de reglas con las reglas cargadas
        # Asignar las reglas cargadas directament
        self.rules = self.rules
        # Añadir el comportamiento de recibir código
        self.add_behaviour(self.ReceiveCodeBehaviour())
