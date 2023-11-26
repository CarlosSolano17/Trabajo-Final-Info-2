#import os 
#from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QSlider,QVBoxLayout,QLabel,QWidget
#import pydicom
#from PyQt5.QtGui import QImage, QPixmap
#import matplotlib.pyplot as plt
#import numpy as np

class Servicio(object):
    def __init__(self):
        self.__usuarios = {}
        #se crea un usuario inicial para arrancar el sistema
        self.__usuarios['123'] = 'Carlos'
        self.__rutas = []
    
    def verificarUsuario(self, u, c):
        try:
            #Si existe la clave se verifica que sea el usuario
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except: #si la clave no existe se genera KeyError
            return False