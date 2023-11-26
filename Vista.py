from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QSlider,QVBoxLayout,QLabel,QWidget


class VentanaPrincipal(QMainWindow):
    #constructor
    def __init__(self, ppal=None):
        super(VentanaPrincipal,self).__init__(ppal)
        loadUi('VentanaLogin1.ui',self)
        self.setup()

    #metodo para configurar las senales-slots y otros de la interfaz
    def setup(self):
        #se programa la senal para el boton
        self.boton_ingresar.clicked.connect(self.accion_ingresar)

        
    def asignarControlador(self,c):
        self.__controlador = c

    def accion_ingresar(self):
        #print("Boton presionado")
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        #esta informacion la debemos pasar al controlador
        resultado = self.__controlador.validar_usuario(usuario,password)
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resultado")

        #se selecciona el resultado de acuerdo al resultado de la operacion
        if resultado == True:
            self.abrirVista2()

        else:
            msg.setText("Usuario no Valido")
            msg.show()
            self.campo_usuario.clear()
            self.campo_password.clear()
        
    def abrirVista2(self):
        self.campo_usuario.clear()
        self.campo_password.clear()
        ventana_ingreso=Vista2(self)
        ventana_ingreso.asignarControlador(self.__controlador)
        self.hide()
        ventana_ingreso.show()

class Vista2(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("Vista2.ui",self)
        self.__ventanaPadre = ppal
        self.__resultado_lista = []
        self.setup()

    def setup(self):
        #se programa la senal para el boton
        self.BotonSalir.clicked.connect(self.accionSalir)

    def asignarControlador(self,c):
        self.__controlador = c

    def accionSalir(self):
        self.hide()
        self.__ventanaPadre.show()