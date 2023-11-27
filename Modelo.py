import numpy as np
import cv2
import pydicom as dc

class Servicio(object):
    def __init__(self,data = None):
        self.__usuarios = {}
        #Usuario!!
        self.__usuarios['123'] = 'Carlos'
        self.__rutas = []

        if data is not None:
            self.asignarDatos(data)
        else:
            self.data = []
            self.sensores = 0
            self.pruebas = 0
            self.etapas = 0
    
    def verificarUsuario(self, u, c):
        try:
            #Si existe la clave se verifica que sea el usuario
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except: #si la clave no existe se genera KeyError
            return False
        
    def asignarDatos(self,data):
        self.data = data
        self.sensores = data.shape[0]
        self.etapas = data.shape[1]
        self.pruebas = data.shape[2]

    def devolverOriginal(self):
        return self.data[:,:,0]
    
    def senalprom(self):
        data = self.data
        x = np.mean(data,0)
        y = np.transpose(x)        
        return y
    
    def senal_reshape(self):
        data=self.data
        reshape=np.reshape(data,(self.sensores,self.etapas*self.pruebas),order = 'F') # Conveirte de 3D a 2D
        return reshape
    
    def senalfiltra(self):
        set=self.data[4,:,5]
        w=(5)
        b=np.zeros((1,202))
        for i in range(0,len(set)):
            valor=set[i]
            if valor >= w/2:
                b[0,i]=w/2
            elif valor< w/2 and valor > -w/3:
                b[0,i]=valor
            elif valor <= -w/3:
                b[0,i]=-w/3     
        return b 
    
    def senalfiltrado(self):
        set=self.data[4,:,5]  
        return set
    
    def devolversig(self,i):
        if i < self.data.shape[2]:
            return self.data[:,:,i]
        else:
            return None
            
    def devolveratras(self,i):
        return self.data[:,:,i]
    
    def lista(self):
        l=[]
        l.append(self.pruebas)
        return l

    def Suavisado(self, kernel_size):
        x = self.__dicom.pixel_array
        smoothed_image = cv2.GaussianBlur(x, (kernel_size, kernel_size), 0)
        return  smoothed_image
    
    def Abrir_dicom(self,i):
        self.__dicom = dc.dcmread(i)
        x = self.__dicom.pixel_array
        return x