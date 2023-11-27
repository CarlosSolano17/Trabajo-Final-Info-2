import typing
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QVBoxLayout,QWidget
import scipy.io as sio
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VentanaPrincipal(QMainWindow):
    #constructor
    def __init__(self, ppal=None):
        super(VentanaPrincipal,self).__init__(ppal)
        loadUi('VentanaLogin1.ui',self)
        self.setup()

    def setup(self):
        self.boton_ingresar.clicked.connect(self.accion_ingresar)

    def asignarControlador(self,c):
        self.__controlador = c

    def accion_ingresar(self):
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        #esta informacion se pasa al controlador
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
        self.BotonSalir.clicked.connect(self.accionSalir)
        self.mat.clicked.connect(self.abrirVistaMat)
        self.dicom.clicked.connect(self.abrirVistaDicom)

    def asignarControlador(self,c):
        self.__controlador = c

    def accionSalir(self):
        self.hide()
        self.__ventanaPadre.show()

    def abrirVistaMat(self):
        ventana_ingreso=VistaMat(self)
        ventana_ingreso.asignarControlador(self.__controlador)
        self.hide()
        ventana_ingreso.show()

    def abrirVistaDicom(self):
        ventana_ingreso=VistaDicom(self)
        ventana_ingreso.asignarControlador(self.__controlador)
        self.hide()
        ventana_ingreso.show()

class MyGraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=2, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)

    def graficar_senal(self, datos):
        self.axes.clear()
        for c in range(datos.shape[0]):
            self.axes.plot(datos[c, :] + c * 25)
        self.axes.set_xlabel('Eje X')
        self.axes.set_ylabel('Eje Y')
        self.draw()

    def graficar_filtrado(self, datos):
        self.axes.clear()
        self.axes.plot(datos[:])
        self.axes.set_xlabel('Eje X')
        self.axes.set_ylabel('Eje Y')
        self.draw()


class VistaMat(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("VistaMat.ui",self)
        self.__ventanaPadre = ppal
        self.j=0
        self.setup()
        
    def asignarControlador(self,c):
        self.__controlador = c

    def setup(self):
        self.campo_grafico = MyGraphCanvas(self, width=6, height=4.7, dpi=100)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.campo_grafico)
        
        self.setLayout(self.layout)

        #se programa la senal para cada boton
        self.ventana_principal.clicked.connect(self.accionSalir)
        self.cargar_senal.clicked.connect(self.cargar)
        self.senal_original.clicked.connect(self.original)
        self.senal_promedio.clicked.connect(self.senal_prom)
        self.senal_reshape.clicked.connect(self.senal_reshapeFun)
        self.senal_filtrado.clicked.connect(self.senal_filtradoFuncion)
        self.siguiente_prueba.clicked.connect(self.adelante)
        self.anterior_prueba.clicked.connect(self.atras)

    def accionSalir(self):
        self.hide()
        self.__ventanaPadre.show()

    def cargar(self):
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Abrir señal","","Todos los archivos (*);;Archivos mat (*.mat);;Python (*.py)")
        
        if archivo_cargado != '':
            #Cargamos los datos
            data = sio.loadmat(archivo_cargado) # Diccionario
            data = data["set"]
            self.__controlador.recibirDatosSenal(data)
            self.x_min = 0
            self.x_max = data.shape[1]
            self.cargar_senal.setStyleSheet("background-color:rgb(248,255,179); border-radius:10px; border: 2px groove gray; border-style:outset")
            self.senal_original.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
            self.senal_promedio.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
            self.senal_reshape.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
            self.senal_filtrado.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
            
    def original(self):
        self.campo_grafico.graficar_senal(self.__controlador.senal_original())
        self.siguiente_prueba.setEnabled(True)
        self.anterior_prueba.setEnabled(True)
        self.cargar_senal.setStyleSheet("background-color:rgb(166, 247, 255); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_original.setStyleSheet("background-color:rgb(248,255,179); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_promedio.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_reshape.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_filtrado.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")

    def senal_prom(self):
        self.campo_grafico.graficar_senal(self.__controlador.senalprom())
        self.siguiente_prueba.setEnabled(False)
        self.anterior_prueba.setEnabled(False)
        self.cargar_senal.setStyleSheet("background-color:rgb(166, 247, 255); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_original.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_promedio.setStyleSheet("background-color:rgb(248,255,179); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_reshape.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_filtrado.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
      
    def senal_reshapeFun(self):
        self.campo_grafico.graficar_senal(self.__controlador.senal_reshapeFun())
        self.siguiente_prueba.setEnabled(False)
        self.anterior_prueba.setEnabled(False)
        self.cargar_senal.setStyleSheet("background-color:rgb(166, 247, 255); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_original.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_promedio.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_reshape.setStyleSheet("background-color:rgb(248,255,179); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_filtrado.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
     
    def senal_filtradoFuncion(self):
        self.campo_grafico.graficar_senal(self.__controlador.senalfiltra())
        self.campo_grafico.graficar_filtrado(self.__controlador.senalfiltradoFun())
        self.siguiente_prueba.setEnabled(False)
        self.anterior_prueba.setEnabled(False)  
        self.cargar_senal.setStyleSheet("background-color:rgb(166, 247, 255); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_original.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_promedio.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_reshape.setStyleSheet("background-color:rgb(255, 213, 241); border-radius:10px; border: 2px groove gray; border-style:outset")
        self.senal_filtrado.setStyleSheet("background-color:rgb(248,255,179); border-radius:10px; border: 2px groove gray; border-style:outset")
       
    def adelante(self):
        p =self.__controlador.lista_data()
        if self.j < p[0]-1:   
            self.j=self.j+1
            self.campo_grafico.graficar_senal(self.__controlador.senal_sig(self.j))
        else:
            texto=("No se puede avanzar más")
            msj=QMessageBox.warning(self, "Alerta", texto,  QMessageBox.Ok, QMessageBox.Cancel) 
            
    def atras(self):
        if self.j > -1:   
            self.j=self.j-1
            self.campo_grafico.graficar_senal(self.__controlador.senal_atras(self.j))
        else:
            texto=("No se puede retroceder más")
            msj=QMessageBox.warning(self, "Alerta", texto,  QMessageBox.Ok, QMessageBox.Cancel) 

class VistaDicom(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("VistaDicom.ui",self)
        self.__ventanaPadre = ppal
        self.setup()

    def asignarControlador(self,c):
        self.__controlador = c

    def setup(self):
        self.BotonSalir.clicked.connect(self.accionSalir)

    def accionSalir(self):
        self.hide()
        self.__ventanaPadre.show()

    
