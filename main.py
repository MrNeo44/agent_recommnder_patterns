
import os
import sys
import asyncio
from dotenv import load_dotenv
from agent.bdi_agent import BDIRecommenderAgent

load_dotenv()

input_queue = asyncio.Queue()
output_queue = asyncio.Queue()
agent = BDIRecommenderAgent(
    os.getenv("BDI_AGENT_JID"),
    os.getenv("BDI_AGENT_PASSWORD"),
    input_queue,
    output_queue
)

async def start_agent():

    await agent.start(auto_register=True)

async def analyze_code_directly(code: str) -> str:
    await input_queue.put(code)
    try:
        pattern = await asyncio.wait_for(output_queue.get(), timeout=30)
        return pattern
    except asyncio.TimeoutError:
        return "ERROR: timeout"

async def main():
    # 1) Arranca el agente
    asyncio.create_task(start_agent())
    await asyncio.sleep(1)  # pequeño delay para asegurar inicio

    # 2) Lee todo stdin
    code = sys.stdin.read()
    print(f"[main.py] Código recibido ({len(code)} chars)", file=sys.stderr)

    # 3) Analiza
    pattern = await analyze_code_directly(code)

    # 4) Imprime resultado (stdout)
    print(pattern, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
