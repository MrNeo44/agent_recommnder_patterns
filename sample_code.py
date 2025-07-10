
class Cliente:
    def __init__(self, nombre, rut, edad, direccion, telefono, email):
        self.nombre = nombre
        self.rut = rut
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def procesar_pago(self, metodo, monto):
        if metodo == "tarjeta":
            print("Procesando pago con tarjeta...")
        elif metodo == "efectivo":
            print("Pagando en efectivo")
        else:
            print("Método no soportado")
