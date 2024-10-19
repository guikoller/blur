import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  './Exemplos/a01 - Original.bmp'
NUM_VIZINHOS = 11

#===============================================================================
def blur(img, vizinhos):
    h, w = img.shape[:2]
    margin = vizinhos // 2
    output = img.copy()
    for y in range(margin, h - margin):
        for x in range(margin, w - margin):
            soma = 0
            for i in range(-margin, margin + 1):
                for j in range(-margin, margin + 1):
                    soma += img[y + i, x + j]
            output[y, x] = soma / (vizinhos * vizinhos)
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

    
#===============================================================================

def main ():
    
    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    img = blurLine (img, NUM_VIZINHOS)
    img = blurCol (img, NUM_VIZINHOS)
    cv2.imwrite ('blur-1.png', img*255)


if __name__ == '__main__':
    main ()

#===============================================================================