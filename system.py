import cv2
import matplotlib.pyplot as plt
import pytesseract as ts
from PIL import Image
import pdf2image
import numpy as np



ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Text:
    def __init__(self,path):
        self.path = path
        
    def img_to_text(self,threshold):

        image = cv2.imread(self.path)
        cv2.imshow("img",image)
        cv2.waitKey(0)
        gray =  cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # cv2.imshow("img",gray)
        # cv2.waitKey(0)
        thres,img = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY)
        # cv2.imshow("img",img)
        # cv2.waitKey(0)
        return ts.image_to_string(img)
        
    def display(self):
        img = cv2.imread(self.path)
        cv2.imshow("image",img)
        cv2.waitKey(0)

    def pdf_to_text(self,threshold):
        images = pdf2image.convert_from_path(self.path,500,poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')

        for i in range(len(images)):
            img_array = np.array(images[i])

            rotated_image = cv2.rotate(img_array, cv2.ROTATE_90_COUNTERCLOCKWISE)
            resized_image = cv2.resize(rotated_image, (800, 600))
            cv2.imshow("koma",resized_image)
            cv2.waitKey(0)

            gray =  cv2.cvtColor(resized_image,cv2.COLOR_RGB2GRAY)
            cv2.imshow("Gray img",gray)
            cv2.waitKey(0)

            thres,img = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY)
            
            cv2.imshow("binarized img",img)
            cv2.waitKey(0)
            return  ts.image_to_string(img) 

book_path = "temp/words.pdf"
obj = Text(book_path)

print(obj.pdf_to_text(150))
