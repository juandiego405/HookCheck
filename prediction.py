import joblib
import numpy as np
import numpy as np
import cv2
import glob
import xlsxwriter
import os


class Procesamiento:

    def __init__(self):

        pass

       


    def prediccion(self,modeloScaler,modelo,path,area):

        self.modeloScaler = modeloScaler
        self.modelo = modelo               
        imageBGR = path
        imageGray = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2GRAY)
        # roiImage = imgBinary[y:y+h,x:x+h]
        roiImageResize = cv2.resize(imageGray,(100,100))
        roiImageReshape = roiImageResize.flatten()
        roiImageReshape = roiImageReshape.reshape(1,-1)
        self.vecScaler = self.modeloScaler.transform(roiImageReshape)
        self.predicciones = self.modelo.predict(self.vecScaler) 
        print(self.predicciones[0])

        if int(self.predicciones[0]) == 0:
            prediccion = 'Buena'

        elif int(self.predicciones[0]) == 1:
            prediccion = 'Mala'
     
        # print(prediccion)
    
                
        # Realizar predicciones en los nuevos datos
        return prediccion

    def loadModel(self,model):
        modelRead = os.path.join('models', model)
        modelo = joblib.load(modelRead)

        return modelo