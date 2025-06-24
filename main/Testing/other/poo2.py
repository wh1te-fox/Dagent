class Coche:
    def __init__(self, matricula, marca, kilometros_recorrido, gasolina):
        self.matricula = matricula
        self.marca = marca
        self.kilometros_recorrido = kilometros_recorrido
        self.gasolina = gasolina

    def avanzar(self, kilometros):
        consumo = kilometros * 0.1

        if self.gasolina >= consumo:
            self.gasolina -= consumo
            self.kilometros_recorrido += kilometros
            print(f"{self.marca} ha recorrido {kilometros} km.")
        else:
            print("Gasolina insuficiente para recorrer esa distancia.")

    def repostar(self, cantidad):
        if cantidad > 0:
            self.gasolina += cantidad
            print(f"Se han añadido {cantidad} litros. Total: {self.gasolina} litros.")
        else:
            print("Cantidad inválida.")

# Uso del objeto
modelo1 = Coche("RS 007", "BMW", 100, 20)
modelo1.avanzar(500)
modelo1.repostar(10)
