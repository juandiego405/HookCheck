import numpy as np
import cv2
import glob
import xlrd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os
import xlsxwriter


class Trainer:
    def __init__(self):

        self.col = 1
        self.row = 0

    def preprocesser(self,workbookName,path,vectorNums,vectorCount):
        self.pathImages = path
        self.vectorNums = vectorNums
        self.vectorCount = vectorCount
        workbook = xlsxwriter.Workbook(os.path.join('dataImages', workbookName))
        workbook.use_zip64()
        worksheet = workbook.add_worksheet()

        for indice, num in enumerate(self.vectorNums):
            self.pathNum = os.path.join(self.pathImages, str(num))
            pathImage = glob.glob(self.pathNum + '/*.png')
            for imgpath in pathImage:
                imageGray = cv2.imread(imgpath,0)
                # roiImage = imgBinary[y:y+h,x:x+h]
                roiImageResize = cv2.resize(imageGray,(100,100))
                roiImageReshape = roiImageResize.flatten()

                for carac in roiImageReshape:
                    worksheet.write(self.row,0,indice)
                    worksheet.write(self.row,self.col, carac)
                    self.col = self.col+1
                self.col = 1 
                self.row = self.row + 1   

        workbook.close()
        self.row = 0
    
    def modelTrainer(self,worbookName,nSize,activation,iter):
        worbookDef = worbookName + ".xlsx"
        worbook = os.path.join('dataImages', worbookDef)
        bookExcel = xlrd.open_workbook(worbook)

        X, Y = self.load_xlsx(bookExcel)
        
        model_scaler = StandardScaler()
        model_scaler.fit(X)
        Xs = model_scaler.transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(Xs, Y, test_size=0.3, random_state=42)

        model_mlp = MLPClassifier(hidden_layer_sizes=(nSize, nSize), max_iter = iter, activation = activation)
        model_mlp.fit(X_train, y_train)
        y_predict = model_mlp.predict(X_test)
        accuracyResult = model_mlp.score(X_test, y_test)
        print(confusion_matrix(y_test,y_predict))

        
        name = activation + "_" + str(nSize) + "_" + str(iter) + worbookName + ".pkl"
        name = os.path.join('models',name)

        name2 = activation + "_" + str(nSize) + "_" + str(iter) + "_Scaler" + worbookName + ".pkl"
        name2 = os.path.join('models',name2)

        print(f"{name2} = {accuracyResult * 100}")

        joblib.dump(model_mlp, name)
        joblib.dump(model_scaler, name2)
        


    def load_xlsx(self,file):
        sh = file.sheet_by_index(0)
        x = np.zeros((sh.nrows, sh.ncols - 1))
        y = []
        for i in range (0,sh.nrows):
            for j in range(0,sh.ncols - 1):
                x[i][j] = sh.cell_value(rowx = i,colx = j+1)
            y.append(sh.cell_value(rowx = i,colx = 0))
        y = np.array(y, np.float32)
        return x, y
    
    
