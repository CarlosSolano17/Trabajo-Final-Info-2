from Vista import VentanaPrincipal
import sys
from PyQt5.QtWidgets import QApplication
from Modelo import Servicio

class Coordinador(object):
    def __init__(self, vista, sistema):
        self.__mi_vista = vista
        self.__mi_sistema = sistema

    def validar_usuario(self, u, p):
        return self.__mi_sistema.verificarUsuario(u,p)
    
    def recibirDatosSenal(self,data):
        self.__mi_sistema.asignarDatos(data)

    def senal_original(self):
        return self.__mi_sistema.devolverOriginal()

    def senalprom(self):
        return self.__mi_sistema.senalprom()
    
    def senal_reshapeFun(self):
        return self.__mi_sistema.senal_reshape()
    
    def senalfiltra(self):
        return self.__mi_sistema.senalfiltra()
    
    def senalfiltradoFun(self):
        return self.__mi_sistema.senalfiltrado()
    
    def senal_sig(self,j):
        return self.__mi_sistema.devolversig(j)
    
    def senal_atras(self,j):
        return self.__mi_sistema.devolveratras(j)
    
    def lista_data(self):
        return self.__mi_sistema.lista()
    
class Principal(object):
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__mi_vista = VentanaPrincipal()
        self.__mi_sistema = Servicio()  
        #hacemos enlaces entre las partes
        self.__mi_coordinador = Coordinador(self.__mi_vista, self.__mi_sistema)
        self.__mi_vista.asignarControlador(self.__mi_coordinador)
           
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())

p = Principal()
p.main() 