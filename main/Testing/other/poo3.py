class Vehiculo:

    def __init__(self, marca, modelo, año, kilometraje):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometraje = kilometraje

    def describir(self): # correccion 
        print(f"{self.marca} {self.modelo} ({self.año}) - {self.kilometraje} km")

    """def describir (self):
        v1 = Vehiculo("BMW", "GT3", 2006, 1050)
        print(v1)"""

    def conducir(self, km):
        self.kilometraje += km
        print(self.kilometraje)

class Coche (Vehiculo):

    def __init__(self, marca, modelo, año, kilometraje, conbustible): 
        # agregar atributo
        super().__init__(marca, modelo, año, kilometraje)
        self.conbustible = conbustible 

    def repostar(self, litros):
        self.conbustible += litros
        
    def conducir(self, km):
        self.conbustible -= 0.1
        print(f"conbustible actual {self.conbustible}")

class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, año, kilometraje, tipo):
        super().__init__(marca, modelo, año, kilometraje)
        self.tipo = tipo
    def conducir(self, km):
        self.kilometraje += km

bmw = Coche("BMW", "Serie 3", 2020, 50000, 20)
bmw.describir()
bmw.conducir(500)
bmw.repostar(10)
bmw.conducir(200)

bici = Bicicleta("Trek", "FX 2", 2022, 1000, "montaña")
bici.describir()
bici.conducir(15)
