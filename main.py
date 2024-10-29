import sys
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  './Exemplos/b01 - Original.bmp'
NUM_VIZINHOS = 11

#===============================================================================

def blur(img, vizinhos):
    h, w, channel = img.shape[:3]
    margin = vizinhos // 2
    output = img.copy()
    for c in range(channel):
        for y in range(margin, h - margin):
            for x in range(margin, w - margin):
                soma = 0
                for i in range(-margin, margin + 1):
                    for j in range(-margin, margin + 1):
                        soma += img[y + i, x + j, c]
                output[y, x, c] = soma / (vizinhos * vizinhos)
    return output


def blurLine(img, vizinhos):
    h, w = img.shape[:2]
    margin = vizinhos // 2
    output = img.copy()
    for y in range(margin, h - margin):
        for x in range(margin, w - margin):
            soma = 0
            for i in range(-margin, margin + 1):
                soma += img[y + i, x]
            output[y, x] = soma / vizinhos
    return output

def blurCol(img, vizinhos):
    h, w = img.shape[:2]
    margin = vizinhos // 2
    output = img.copy()
    for y in range(margin, h - margin):
        for x in range(margin, w - margin):
            soma = 0
            for i in range(-margin, margin + 1):
                soma += img[y, x+i]
            output[y, x] = soma / vizinhos
    return output

def blurXY(img, vizinhos):
    output = img.copy()
    output = blurLine(output, vizinhos)
    output = blurCol(output, vizinhos)
    return output

def integral(img):
    h, w, c = img.shape[:3]
    output = img.copy()
    
    for channel in range(c):
        for y in range(0, w):
            output[0, y, channel] = img[0, y, channel]
            for x in range(1, h):
                output[x, y, channel] = img[x, y, channel] + output[x - 1, y, channel]
    
    for channel in range(c):
        for y in range(1, w):
            for x in range(0, h):
                output[x, y, channel] = output[x, y, channel] + output[x, y-1, channel]
            
    return output   

def regionSum(integral_img, x, y, margin, c):
    return  (
                integral_img[x - margin, y - margin, c] +
                integral_img[x + margin, y + margin, c] -
                integral_img[x + margin, y - margin, c] -
                integral_img[x - margin, y + margin, c]
            )

def blur_integral(img, vizinhos):
    h, w, c = img.shape[:3]
    area = vizinhos ** 2
    margin = int(vizinhos / 2)
    output = img.copy()
    integral_img = integral(img)
    for channel in range(c):
        for y in range(margin, w - margin):
            for x in range(margin, h - margin):    
                sum_region = sum_region = regionSum(integral_img, x, y, margin, channel)
                output[x, y, channel] = sum_region / area

    return output
        
#===============================================================================
def main ():
    
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    
    img = img.reshape ((img.shape [0], img.shape [1], img.shape [2]))
    img = img.astype (np.float32) / 255

    img_blur = blur(img, NUM_VIZINHOS)
    cv2.imwrite ('blur.png', img_blur*255)
    print('blur')
    
    img_blurXY = blurXY(img,NUM_VIZINHOS)
    cv2.imwrite ('blurXY.png', img_blurXY*255)
    print('blurXY')
    
    img_integral = blur_integral(img,NUM_VIZINHOS)
    cv2.imwrite ('blurIntegral.png', img_integral*255)
    print('Blur Integral')
    
    csv_blur = cv2.blur(img, (NUM_VIZINHOS, NUM_VIZINHOS))
    cv2.imwrite ('blurCV.png', csv_blur*255)
    print('blurCV')

if __name__ == '__main__':
    main ()
#===============================================================================