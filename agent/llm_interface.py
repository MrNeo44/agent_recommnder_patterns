import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Obtener la clave de API de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la clave de API está configurada
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY no configurada. Se detendrá la ejecución.")

# Asignar la clave de API a la librería OpenAI
openai.api_key = openai_api_key


def query_llm(code: str, smells: list) -> str:
    """Consulta al modelo LLM para sugerir un patrón de diseño dado el código y los smells."""
    prompt = f"""Eres un experto en patrones de diseño. Dado el siguiente código y los olores de código detectados, responde solo con el nombre del patrón de diseño adecuado.

    Código:
    {code}

    Olores de código detectados: {', '.join(smells)}

    ¿Qué patrón de diseño corresponde a este código? Solo responde con el nombre del patrón sin explicar ni añadir texto adicional."""

    try:
        # Realiza la consulta al LLM usando el modelo gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usar gpt-3.5-turbo o gpt-4 si tienes acceso
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.5
        )

        # Obtener la respuesta del modelo
        message_content = response['choices'][0]['message']['content']

        # Limpiar la respuesta para obtener solo el nombre del patrón
        pattern = message_content.strip()

        # Verificar si la respuesta es válida
        if "patrón" in pattern.lower():
            pattern = pattern.split(":")[0].strip()  # Asegurarnos de que solo el nombre sea extraído

        print(f"Patrón devuelto por el LLM: {pattern}")
        return pattern

    except openai.OpenAIError as e:
        print(f"Error al consultar OpenAI: {e}")
        return f"Error al obtener patrón: {e}"

    except Exception as e:
        print(f"Error inesperado: {e}")
        return f"Error inesperado: {e}"
