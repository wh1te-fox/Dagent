class Coche:

    def __init__(self, matricula, marca, 
                 kilometros_recorrido, gasolina):
        
        self.matricula = matricula
        self.marca = marca
        self.kilometros_recorrido = kilometros_recorrido
        self.gasolina = gasolina
        
  
    def avanza (self, kilometros_recorrer):
        self.kilometros_recorrido += kilometros_recorrer
        self.gasolina -= (kilometros_recorrer * 0.1)

        print (f"recorrido {self.kilometros_recorrido}\n"
               f"gasolina restante: {self.gasolina}")
        
        if self.gasolina  <= 0:
            print("Es necesario repostar para recorrer la cantidad de kilimetros")
            self.reposar() # llama a una metodo por medio de self.funcion()
            
    def reposar(self):
        self.gasolina += int(input("Ingrese la gasolina: "))
        return print(f"{self.gasolina} actual")
      

modelo1 = Coche("RS 007", "BMW", 200, 10)
modelo1.avanza(200)
print(modelo1.marca)