import numpy as np
import cv2 
import os
from prediction import Procesamiento


class Camera():

    def __init__(self):
        self.cap = None
        self.frame = None
        self.ret = None

    def create_capture(self):
        self.cap = cv2.VideoCapture(1)
        return self.cap

    def open_camera(self,capture):
        T= Tagger()

        while capture.isOpened():
            self.ret, self.frame = capture.read()     
            
            cv2.imshow ("frame", self.frame)
            
            T.tagging(self.frame,carpeta="dataset_Z16",estado="malas")            
 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                break

    def model_read(self,capture):
        bandera = True
        Buenas = 0
        Malas = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_color = (255, 255, 255)  # Blanco en formato BGR
        font_thickness = 1

        P=Procesamiento()
        T=Tagger()

        modelScaler = P.loadModel('relu_100_1000_ScalerdataImages_Z16.pkl')
        model = P.loadModel('relu_100_1000dataImages_Z16.pkl')

        while capture.isOpened():
            self.ret, self.frame = capture.read()    
            
            
            imgBin = T.binarizeImg(self.frame)
            contours, hier = cv2.findContours(imgBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                    # cv2.imshow("imgBin",imgBin)
            if len(contours) > 0:
                for i in range(len(contours)):
                    x, y, w, h = cv2.boundingRect(contours[i])
                    area = w*h
                    if area > 3000 and area < 30000:
                        imgCut = T.roiImg(self.frame,x,y,w,h)
                        
                        cv2.imshow("cut",imgCut)
                        
                        if ((x) >= 260) and ((x+w)<420) and ((y)>100 and (y+h)<300 ) and bandera == True:
                            print(imgCut.shape[:2])
                            prediccion = P.prediccion(modeloScaler=modelScaler,modelo=model,path=imgCut,area=area)
                            print(prediccion)
                            if prediccion == "Buena":
                                Buenas+=1
                                
                                print(f'Buenas #: {Buenas}')
                            elif prediccion == "Mala":
                                Malas+=1
                                print(f'Malas #: {Malas}')
                       
                            bandera = False

                            # print(f'area: {area}')
                        elif ((x+w) > 420):
                            bandera = True

                        
            text = f'Buenas: {Buenas} Malas: {Malas}'
            cv2.putText(self.frame, text, (50, 20), font, font_scale, font_color, font_thickness)
            cv2.imshow ("frame", self.frame)
            
            # T.tagging(self.frame,"polea")           
            if cv2.waitKey(1) & 0xFF == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                break

            # elif cv2.waitKey(1) & 0xFF == ord('s'):

class Tagger():

    def __init__(self):
        self.indice = 0
        

    def tagging(self,frame,carpeta,estado):
        
        imgBin = self.binarizeImg(frame)
        contours, hier = cv2.findContours(imgBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        frame2= frame
        cv2.line(frame2,(260,0),(260,620),(255,255,255))
        cv2.line(frame2,(420,0),(420,620),(255,255,255))
        cv2.line(frame2,(0,100),(620,100),(255,255,255))
        cv2.line(frame2,(0,300),(620,300),(255,255,255))
        cv2.imshow("framecopy",frame2)
        cv2.imshow("imgBin",imgBin)
        if len(contours) > 0:
            for i in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[i])
                area = w*h
                # print(area)
                if area > 3000 and area < 30000:
                    imgCut = self.roiImg(frame,x,y,w,h)
                    cv2.imshow("cut",imgCut)
                    # print("x: ", x)
                    # print("w: ", w)

                    if ((x) >= 260) and ((x+w)<420) and ((y)>100 and (y+h)<300 ):

                        dir = carpeta + "_"+ estado + "_" + str(self.indice) + ".png"
                        if carpeta == 'dataset_T10':
                            if estado == 'buenas':
                                ruta_completa = os.path.join(carpeta,"Buenas_T10", dir)
                            elif estado == "malas":
                                ruta_completa = os.path.join(carpeta,"Malas_T10", dir)

                        
                        elif carpeta == 'dataset_T13':
                            if estado == 'buenas':
                                ruta_completa = os.path.join(carpeta,"Buenas_T13", dir)
                            elif estado == "malas":
                                ruta_completa = os.path.join(carpeta,"Malas_T13", dir)

                        elif carpeta == 'dataset_Z16':
                            if estado == 'buenas':
                                ruta_completa = os.path.join(carpeta,"Buenas_Z16", dir)
                            elif estado == "malas":
                                ruta_completa = os.path.join(carpeta,"Malas_Z16", dir)

                        elif carpeta == 'dataset_Arandelas':
                            if estado == 'buenas':
                                ruta_completa = os.path.join(carpeta,"Buenas_Arandelas", dir)
                            elif estado == "malas":
                                ruta_completa = os.path.join(carpeta,"Malas_Arandelas", dir)  

                        elif carpeta == 'datasetPrueba':
                            if estado == 'buenas':
                                ruta_completa = os.path.join(carpeta,"Buenas", dir)
                            elif estado == "malas":
                                ruta_completa = os.path.join(carpeta,"Malas", dir)                     
                        
                        cv2.imwrite(ruta_completa,imgCut)
                        self.indice+=1
                        print(f"tomando foto: {self.indice}")
                        print(f'area: {area}')
                        

    def roiImg(self,img,x1,y1,w,h):
            roiImage = img[y1:y1+h, x1:x1+w] 
            return roiImage

    def binarizeImg(self,img):
        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, imgBin = cv2.threshold(imgGrey,30,255, cv2.THRESH_BINARY)
        return imgBin
    


        
