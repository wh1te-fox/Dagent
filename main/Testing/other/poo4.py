class CuentaBancaria:

    def __init__(self, dinero):
        self.dinero = dinero

    def depositar (self, deposito):
        print (f"el dinero depositado es de: {self.dinero + deposito}")
    def retirar (self, retiro):
        if self.dinero > 0:
            print (f"el dinero retidaro es de: {retiro}, restan: {self.dinero - retiro} ")
        else:
            print("no tiene sufiebte dinero para retirar")
    def consultar_saldo(self):
        print(f"su dinero actual es de {self.dinero}")
    