import numpy as np


def converte_adjacente(arr, lin, col):
    linha, colun = arr.shape
    arr[lin][col] = 2

    for i in range(-1,2):
        for j in range(-1,2):

            nova_lin = lin + i
            nova_col = col + j
            #print('.')
            if nova_lin >= 0 and nova_lin < linha and nova_col >=0 and nova_col < colun:
                #print('.')
                if arr[nova_lin][nova_col] == 1:
                    converte_adjacente(arr,nova_lin,nova_col)



def conta_ilhas(arr):
    lin, col = arr.shape
    ilhas=0
    for i in range(lin):
        for j in range(col):

            if arr[i][j] == 1:
                #print(',')    
                converte_adjacente(arr,i,j)
                ilhas=ilhas+1

    return ilhas

    
matr = np.array([[1,1,1,1,0],
                 [1,0,0,0,0],
                 [1,0,1,1,1],
                 [1,0,1,0,0],
                 [0,0,1,0,1]])
lin, col = matr.shape

print(matr)
print(conta_ilhas(matr))
print(matr)
