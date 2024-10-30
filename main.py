import sys
import numpy as np
import cv2
import math

#===============================================================================

INPUT_IMAGE =  './Exemplos/a01 - Original.bmp'
NUM_VIZINHOS = 5

#===============================================================================

def blur(img, vizinhos):
    h, w, channel = img.shape[:3]
    margin = vizinhos // 2
    output = img.copy()
    area = vizinhos * vizinhos
    for c in range(channel):
        for y in range(margin, h - margin):
            for x in range(margin, w - margin):
                soma = 0
                for i in range(-margin, margin + 1):
                    for j in range(-margin, margin + 1):
                        soma += img[y + i, x + j, c]
                output[y, x, c] = soma / area
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
                integral_img[x - margin - 1, y - margin - 1, c] +
                integral_img[x + margin    , y + margin    , c] -
                integral_img[x + margin    , y - margin - 1, c] -
                integral_img[x - margin - 1, y + margin    , c]
            )

def blur_integral(img, vizinhos):
    h, w, c = img.shape[:3]
    area = vizinhos * vizinhos
    margin = vizinhos // 2
    output = img.copy()
    integral_img = integral(img)
    for channel in range(c):
        for y in range(margin, w - margin):
            for x in range(margin, h - margin):    
                sum_region = sum_region = regionSum(integral_img, x, y, margin, channel)
                output[x, y, channel] = sum_region / area

    return output

def compare(img, img2):
    output = img.copy()
    output = img*255 - img2*255
    return cv2.normalize(output, None, 0, 1, cv2.NORM_MINMAX)
    
#===============================================================================
def main ():

    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    
    img = img.reshape ((img.shape [0], img.shape [1], img.shape [2]))
    img = img.astype (np.float32) / 255

    csv_blur = cv2.blur(img, (NUM_VIZINHOS, NUM_VIZINHOS))
    cv2.imwrite ('blurCV.png', csv_blur*255)
    print('blurCV')
    
    img_blur = blur(img, NUM_VIZINHOS)
    cv2.imwrite ('blur.png', img_blur*255)
    print('blur')
    comparaBlur = compare(csv_blur, img_blur)
    cv2.imwrite ('comparaBlur.png', comparaBlur*255)
    
    img_blurXY = blurXY(img,NUM_VIZINHOS)
    cv2.imwrite ('blurXY.png', img_blurXY*255)
    print('blurXY')
    comparaBlurXY = compare(csv_blur, img_blurXY)
    cv2.imwrite ('comparaBlurXY.png', comparaBlurXY*255)
    
    img_integral = blur_integral(img,NUM_VIZINHOS)
    cv2.imwrite ('blurIntegral.png', img_integral*255)
    print('Blur Integral')
    comparaItegral = compare(csv_blur, img_integral)
    cv2.imwrite ('comparaItegral.png', comparaItegral*255)

if __name__ == '__main__':
    main ()
#===============================================================================