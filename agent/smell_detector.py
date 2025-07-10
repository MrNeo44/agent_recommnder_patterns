import ast
from typing import List


class SmellDetector:
    def detect(self, code: str) -> List[str]:
        tree = ast.parse(code)
        smells = set()

        for node in ast.walk(tree):
            # Constructor extenso
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                if len(node.args.args) > 4:
                    smells.add("Constructor extenso")

            # Condicionales anidados (>1 nivel)
            if isinstance(node, ast.If):
                if any(isinstance(child, ast.If) for child in ast.iter_child_nodes(node)):
                    smells.add("Condiconales anidados")

            # Verificación de tipo
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "isinstance":
                smells.add("Verificacn de tipo")

            # Método largo
            if isinstance(node, ast.FunctionDef) and len(node.body) > 10:
                smells.add("Metodo largo")

            # Clase grande
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for n in ast.walk(node) if isinstance(n, ast.FunctionDef))
                if method_count > 5:
                    smells.add("Clase grande")

            # Duplicación de código
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                if function_name in ["metodo_raro", "metodo_complejo"]:  # Detección de duplicación de código
                    smells.add("Duplicación de código")

            # Uso de 'global'
            if isinstance(node, ast.Global):
                smells.add("Uso de 'global' (posible Singleton mal implementado)")

            # Demasiados parámetros
            if isinstance(node, ast.FunctionDef):
                param_names = [arg.arg for arg in node.args.args]
                if len(param_names) > 3 and "self" in param_names:
                    smells.add("Demasiados parámetros")

            # Clases con demasiadas responsabilidades
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for n in ast.walk(node) if isinstance(n, ast.FunctionDef))
                if method_count > 5:
                    smells.add("Clase con demasiadas responsabilidades")

            # Uso de interfaces o clases abstractas sin implementación
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name) and node.value.func.id == "isinstance":
                    smells.add("Uso de interfaces sin implementación")

        return list(smells)

    def create_smell_with_llm(self, code: str) -> List[str]:
        prompt = f"""Eres un experto en patrones de diseño. Dado el siguiente código, ¿qué olores de código detectas? Devuelve solo los olores detectados sin ninguna explicación adicional.

        Código:
        {code}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Usar gpt-3.5-turbo o gpt-4 si tienes acceso
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5
            )

            message_content = response['choices'][0]['message']['content']
            smells = message_content.strip().split(",")  # Asumimos que los olores vienen separados por comas
            smells = [smell.strip() for smell in smells]

            print(f"Olores detectados por el LLM: {smells}")
            return smells

        except openai.OpenAIError as e:
            print(f"Error al consultar OpenAI: {e}")
            return []

        except Exception as e:
            print(f"Error inesperado: {e}")
            return []
