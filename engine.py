import pandas as pd
import requests
import json
import cv2
import pdf2image
import numpy as np
import io

model_id = 'a48077e4-08ec-4341-952b-364a0cdcdc1b'
url = 'https://app.nanonets.com/api/v2/OCR/Model/' + model_id + '/LabelFile/'

ac_no = []
name = []
address = []
bank = []
description = []
debit = []
credit = []
balance = []
date = []





class Exopy:

    def __init__(self,img_path):
        self.img_path = img_path
    
    def for_pdf(self,image):
        responses = []
        
        for i in range(len(image)):
            image_data = image[i].convert('RGB')
            byte_array = io.BytesIO()
            image_data.save(byte_array, format='PNG')
            byte_array.seek(0)

            response = requests.post(url, auth=requests.auth.HTTPBasicAuth('1586d6e7-01c8-11ee-ab5f-9a31cf85287d', ''), files={'file': byte_array})
            data = response.json()
            print(data)
            responses.append(data)
        
        print("responses completed")
        return responses
    
        
    
    def json_response(self):
        responses = []
        image_path = self.img_path

        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('1586d6e7-01c8-11ee-ab5f-9a31cf85287d', ''), files={'file': image_data})

        
        data = response.json() 
        responses.append(data)
        return responses
    
    def touch(self,length):
        Names= []
        Ac_No = []
        for i in range(length):
            Names.append(name[0])
            Ac_No.append(ac_no[0])
        return Names,Ac_No
    def pdf_img_text(self):
        images = pdf2image.convert_from_path(self.img_path,500,poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')
        
        dictionary = self.for_pdf(images)
        for doc in dictionary:
            results = doc['result']
            data = results[0]
            prediction = data['prediction']
            print("dicitionary loop ")
            for i in prediction:
                print("running")
                if i['label']== 'Account_name':
                    name.append(i['ocr_text'])
                elif i['label'] == 'Account_number':
                    ac_no.append(str(i['ocr_text']))
            
            j = i['cells']

            for data in j:
                if data['label']=='Description':
                    description.append(data['text'])
                elif data['label']== 'Debit':
                    debit.append(data['text'])
                elif data['label'] == 'Credit':
                    credit.append(data['text'])
                elif data['label'] == 'Balance':
                    balance.append(data['text'])
                elif data['label'] == 'Transaction_date':
                    date.append(data['text'])
    def img_text(self):
        dictionary = self.json_response()
        
        results = dictionary['result']
        data = results[0]
        prediction = data['prediction']

        for i in prediction:
            if i['label']=='Account_address':
                address.append(i['ocr_text'])
            elif i['label']== 'Account_name':
                name.append(i['ocr_text'])
            elif i['label'] == 'Bank_name':
                bank.append(i['ocr_text'])
            elif i['label'] == 'Account_number':
                ac_no.append(str(i['ocr_text']))
        
        j = i['cells']

        for data in j:
            if data['label']=='Description':
                description.append(data['text'])
            elif data['label']== 'Debit':
                debit.append(data['text'])
            elif data['label'] == 'Credit':
                credit.append(data['text'])
            elif data['label'] == 'Balance':
                balance.append(data['text'])
            elif data['label'] == 'Transaction_date':
                date.append(data['text'])

    def dictinaries(self):
        self.img_text()
        Names,Ac_No = self.touch(len(description))
        
        eng_date = self.eng_date()
        data = dict()

        data = {'Name':Names,'Account_No':Ac_No,'Description':description,'Debit':debit,'Credit':credit,'Balance':balance,'Date':eng_date}
        print(len(Names))
        print(len(Ac_No))
        print(len(description))
        print(len(debit))
        print(len(credit))
        print(len(balance))
        print(len(eng_date))
        return data
        
    def pdf_dictinaries(self):
        self.pdf_img_text()
        Names,Ac_No = self.touch(len(description))
        
        eng_date = self.eng_date()
        data = dict()
        print(date)
        data = {'Name':Names,'Account_No':Ac_No,'Description':description,'Debit':debit,'Credit':credit,'Balance':balance,'Date':date}
        print(len(Names))
        print(len(Ac_No))
        print(len(description))
        print(len(debit))
        print(len(credit))
        print(len(balance))
        print(len(eng_date))
        return data

    def eng_date(self):
        eng_date = []
        for j in range(len(date)):
            if j%2!=0:
                eng_date.append(date[j])
        return eng_date
        
    def pdf_to_excel(self,file_name):
        
        data = self.pdf_dictinaries()
        df = pd.DataFrame(data)
        return df.to_excel(file_name,index=False)
    
    def img_to_excel(self,file_name):
        data = self.dictinaries()
        df = pd.DataFrame(data)
        return df.to_excel(file_name,index=False)


Input = "statements.pdf"
obj = Exopy(Input)
obj.pdf_to_excel("data90.xlsx")