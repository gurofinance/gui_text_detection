import cv2
import pytesseract 
import re
import numpy as np 
import tempfile

pytesseract.pytesseract.tesseract_cmd="C:/program Files/Tesseract-OCR/tesseract.exe"

cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


# faces = cascade.detectMultiScale(img , scaleFactor=1.1, minNeighbors=5, minSize=(5,5))
# print(faces)
config  = r'--oem 1 --psm 6 outoutbase digits'

def convert_gray_color(file_path):
    img = cv2.imread(file_path)
    gray_image = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    
    # cv2.imshow('이미지', gray_image)
    # cv2.waitKey(0)
    return gray_image

def image_smoothing(img):
    ret, th1 = cv2.threshold(img , 127 , 255, cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(th1 , (1,1),0)
    # cv2.imshow('img', img)
    # cv2.imshow('th1', th1)
    # cv2.imshow('blur', blur)
    # cv2.waitKey(0)
    
    return blur


#text 정제처리
def clean_text(read_data):
    text = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ!』\\"|\(\)\[\]\<\>`\"…》£"¢¥"Ÿ«éȮϽñٶϴ»「—©]', '', read_data)
    return text

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, flags=0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255 , cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY, 41, 3)
    kernal = np.ones((1,1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel=kernal) #노이즈 제거
    closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel=kernal) #노이즈 제거
    img  = image_smoothing(img)
    or_image = cv2.bitwise_or(img, closing)
    # print(or_image)
    # cv2.imshow('얼굴인식부분', or_image)
    # cv2.waitKey(0)
    return or_image


def rectangle_detect(file_fath, lang='kor'):
    gray_image = convert_gray_color(file_fath)
    faces = cascade.detectMultiScale(gray_image , scaleFactor=1.1, minNeighbors=5, minSize=(5,5))
    for i in faces:
        x , y ,w ,h =i
        img_rec = cv2.rectangle(gray_image, (x, y), (x+w, y+h), (0,0,255), -1)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False , suffix='.jpg')
    temp_file_name = temp_file.name
    cv2.imwrite(temp_file_name , img_rec)
    
    smooth_image = remove_noise_and_smooth(temp_file_name)
    # cv2.imshow("face rectangle", img_rec)  
    # cv2.waitKey(0)
    num_boxes = pytesseract.pytesseract.image_to_data(smooth_image  , lang=lang, config=config)
    text = pytesseract.pytesseract.image_to_string(gray_image , lang=lang)
    
    num_list=[]
    file_name = ''
    for  x , b in enumerate(num_boxes.splitlines()):
        
        if x !=0 :
            b = b.split()
            # print("#")
            # print(b)
            if len(b)== 12 and len(b[11])>11:
                num_list.append(b)
    print(num_list)
    
    for i in range(len(num_list)):
        number = num_list[i][11]
        # print(number)
        x ,y ,w,h = int(num_list[i][6]), int(num_list[i][7]), int(num_list[i][8]), int(num_list[i][9])
        img_rec = cv2.rectangle(gray_image, (x, y), (x+w, y+h), (0,0,255), -1)
        # print(len(number))
        if len(number) >=13 and len(number) <=16:
            if '-' in number:
                naming_number = clean_text(num_list[i][11])
                for i in range(len(naming_number)):
                    if i%2 == 0:
                        file_name +=  naming_number[i]
                print(file_name)     
    # print(text)
    if file_name:
        cv2.imwrite(f'result_image/{file_name}.jpg', gray_image)
        with open(f'result_image/{file_name}.txt', 'w', encoding="UTF-8") as f :
            f.write(text)
            f.close()
        return f'result_image/{file_name}'
    
    else:
        import string
        import random
        number_of_strings = 5
        length_of_string = 8
        for x in range(number_of_strings):
            temp_filename = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        print(temp_filename)
        cv2.imwrite(f'result_image/{temp_filename}.jpg' , gray_image)
        with open(f'result_image/{temp_filename}.txt', 'w', encoding="UTF-8") as f :
            f.write(text)
            f.close()
        return f'result_image/{temp_filename}'
    

    
# config  = r'--oem 1 --psm 6 outoutbase digits'

# num_boxes = pytesseract.pytesseract.image_to_data(img  , lang='kor', config=config)
# print(type(num_boxes))
# for  x , b in enumerate(num_boxes.splitlines()):
#     print(b)

# img = convert_gray_color('images/id_6.jpg')
# image_smoothing(img)
# remove_noise_and_smooth('images/id_6.jpg')
# rectangle_detect('images/id_4.jpg', lang='kor')