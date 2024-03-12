import numpy as np
import cv2
from camera_Tag import Camera
from train import Trainer
from prediction import Procesamiento

#####Colocar las direcciones de path de imagenes

# pathImages = r"C:/Users/juand/OneDrive/Documentos/Universidad/10 semestre/vision artificial/TrabajoFinal/TrabajoFinal/dataset_Arandelas"
# pathImages = r"C:/Users/juand/OneDrive/Documentos/Universidad/10 semestre/vision artificial/TrabajoFinal/TrabajoFinal/dataset_T10"
pathImages = r"C:/Users/juand/OneDrive/Documentos/Universidad/10 semestre/vision artificial/TrabajoFinal/TrabajoFinal/dataset_Z16"
# pathImages = r"C:/Users/juand/OneDrive/Documentos/Universidad/10 semestre/vision artificial/TrabajoFinal/TrabajoFinal/datasetPrueba"

vectorNums = ['Buenas_Z16','Malas_Z16']
vectorCount = [0,0]
def main():
    camera = Camera()
    capture = camera.create_capture()
    # camera.open_camera(capture=capture) ###OJO TRIPLEMK SOLO SE DESCOMENTA PARA TAGGEAR
    camera.model_read(capture=capture)
    





    T = Trainer()
    # T.preprocesser(workbookName='dataImages_Z16.xlsx',path=pathImages,vectorNums=vectorNums,vectorCount=vectorCount)
    # T.modelTrainer(worbookName='dataImages_Z16',nSize=100,activation='relu',iter=1000)





    # # for i in range(200):
    # prediccion = P.prediccion(modeloScaler=modelScaler,modelo=model,path=)
    # print(prediccion)
    #     prediccion = P.prediccion(modeloScaler=modelScaler,modelo=model,path=pathTuerca)
    #     print(prediccion)
    #     prediccion = P.prediccion(modeloScaler=modelScaler,modelo=model,path=pathArandelas)
    #     print(prediccion)

if __name__ == "__main__":
    main()