import cv2
import time as t
import os
import tkinter as tk
from PIL import Image
from pyzbar.pyzbar import decode
# from sympy import true

def gui(text_):
    root = tk.Tk()
    root.geometry('720x100')
    root.minsize(200,100)
    lab1 = tk.Label(text=f"{text_}",font=('Arial',25))
    lab1.pack()
    root.mainloop()
    pass

cap=cv2.VideoCapture(0)
while True:
    ret,fm = cap.read()
    cv2.imshow('camera - q for exit',fm)
    cv2.waitKey(100)
    
    if ret:
        cv2.imwrite('/tmp/WIFI_QR_Scan.png',fm)
        data = decode(Image.open('/tmp/WIFI_QR_Scan.png'))
        data=str(data)
        find =None
        if (('P' in data)or(('D'or'd') in data)):
            # print('QR code Found')
            break
            # ret,frame = cap.read()
        
        if cv2.waitKey(1) & 0xFF == ord("q") or 0xFF == ord('Q'):
            break
store=[]
store_pwd=[]
store_uid=[]

txt =None
txt_uid =None
txt_pwd =None

try:
    find = data.index('P:')
except:
    pass
if find:
    try:
        #Passwd
        find = data.index('P:')
        find2= find
        while True:
            find2 = find2+1
            # print(data[find2])
            if data[find2]==';':
               break

        # print("passwd :" , end ='')
        for i in range (find,find2-2):
            # print(data[i+2],end='') 
            store_pwd.append(data[i+2])
        txt_pwd=''.join(store_pwd)
        
        
        #UID name 
        find = data.index('S:')
        find2= find
        while True:
            find2 = find2+1
            # print(data[find2])
            if data[find2]==';':
            #    print(find2)
               break
        for i in range (find,find2-2):
            # print(data[i+2],end='') 
            store_uid.append(data[i+2])
            txt_uid=''.join(store_uid)
        
        cap.release() 
        os.system(f'nmcli d wifi connect "{txt_uid}" password  "{txt_pwd}"')
        print(f'UID :{txt_uid}')     
        print(f'paswd :{txt_pwd}')
        
        # gui('Wifi connected')  
    except:
        print("Please re-scan not a wifi QR or bluary QR")
else:
    # print("\t\t\t{ Other than Wifi : }\n")
    try:
        find=data.index("'")
        find2=data.index(',')
        print("Full QR Data \n\t"+data)
        print("\nQR Data : \t")
        for i in range (find,find2):
                print(data[i],end='')
                store.append(data[i])
        txt=''.join(store)
        # gui(txt)   
    except:
        print("Error while reading QR")

     

#Delete picture 
os.system('rm /tmp/WIFI_QR_Scan.png')