import cv2
import numpy as np
import os

nome_arq = 'modelo_dados.png'

def detecta_quadrados_com_borda(nome_arq):
    try: os.listdir('./imagens_tabelas')
    except : os.mkdir('./imagens_tabelas')

    imgs_para_apagar = [ x for x in os.listdir('./imagens_tabelas') if ('ROI' in x)]
    for i in imgs_para_apagar : os.remove(f'./imagens_tabelas/{i}')

    img = cv2.imread(f'./{nome_arq}')
    imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)

    kernel = np.ones((11,21),np.uint8)
    closing = cv2.morphologyEx(thrash, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(closing,kernel,iterations = 1)

    contours , hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    lista_retangulos = [ 
        cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True) for c in contours 
        if len(cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True)) == 4
    ]

    lista_index_retirar = []

    for i in range(len(lista_retangulos)) :
        approx_avaliado = lista_retangulos[i]
        x1, y1 , w1, h1 = cv2.boundingRect(approx_avaliado)
        for x in range(len(lista_retangulos)):
            if i!=x :
                approx = lista_retangulos[x]
                x, y , w, h = cv2.boundingRect(approx)
                if ( x1>x and y1>y and x1+w1<x+w and y1+h1<y+h ):
                    lista_index_retirar.append(i)
                    break
                    
    lista_retangulos = [ lista_retangulos[x] for x in range(len(lista_retangulos)) if not(x in lista_index_retirar) ]

    print(len(lista_retangulos),'Tabelas identificadas.')

    image_number = 0
    for approx in lista_retangulos:
        x, y , w, h = cv2.boundingRect(approx)
        borda = 3
        ROI = img[ y+borda : y-borda+h, x+borda : x-borda+w ]
        cv2.imwrite(f'./imagens_tabelas/ROI_{image_number}.png', ROI)
        image_number += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2) # desenha o contorno 

        if 1.05 > float(w)/h >= 0.95 :
            cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
            cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        
    # cv2.imshow('image real', img)
    # cv2.imshow('image cinza', imgGry)
    # cv2.imshow('mascara', thrash)
    # cv2.imshow('image com closing', closing)
    # cv2.imshow('image dilatada', dilation)
    # cv2.imshow('image com erosão', erosion)
    # cv2.waitKey()

if __name__ == "__main__":
    detecta_quadrados_com_borda(nome_arq)