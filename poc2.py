global global_var

class MiClase:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def metodo1(self):
        global global_var
        global_var = self.a + self.b
        print(f"El resultado es: {global_var}")

    def metodo2(self):
        global global_var
        print(f"Accediendo a la variable global: {global_var}")
        print("algo")

# Instanciando la clase y utilizando los métodos
objeto = MiClase(5, 236326)
objeto.metodo1()
objeto.metodo2()