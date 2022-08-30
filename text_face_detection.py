import cv2
import pytesseract 

pytesseract.pytesseract.tesseract_cmd="C:/program Files/Tesseract-OCR/tesseract.exe"

cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

img = cv2.imread('images/id_2.jpg' ,cv2.IMREAD_COLOR )
print(img.shape)
faces = cascade.detectMultiScale(img , scaleFactor=1.1, minNeighbors=5, minSize=(5,5))
print(faces)

for i in faces:
    x , y ,w ,h =i
    img_rec = cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), -1)
    # cv2.imshow("face rectangle", img_rec)    
    cv2.imwrite("test.jpg" , img_rec)
    
config  = r'--oem 1 --psm 6 outoutbase digits'

num_boxes = pytesseract.pytesseract.image_to_data(img  , lang='kor', config=config)
print(type(num_boxes))
for  x , b in enumerate(num_boxes.splitlines()):
    print(b)