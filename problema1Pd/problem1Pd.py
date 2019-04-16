from operator import itemgetter
import datetime

def mochila(capacidade, valxpeso, tamanho, M):
    K = [[0 for x in range(capacidade+1)] for x in range(tamanho+1)]
    S = [[None for x in range(capacidade+1)] for x in range(tamanho+1)]
    

    for i in range(tamanho + 1):
        
        #print( M[i-1][0],  M[i-2][0])
        for w in range(capacidade + 1):
            
            indiceAnt = str(S[i-1][w])
            indiceAnt = (indiceAnt.replace('[','').replace(']','')).split(',') 
            #print(indiceAnt[0])
            #indiceAnt = indiceAnt[1:len(indiceAnt)-1]
            

            if indiceAnt[0] != 'None':
                #print('Es un numero')
                pAnteri = M[int(indiceAnt[0])][2]
            else:
                pAnteri = '00:00'

            #pAnteri = M[][2]
            pActual = M[i-1][1] 
            #print('K[',i,'][',w,']',pActual, pAnteri)
            #and isNoOverlapped(pAnteri,pActual)
            if i == 0 or w == 0 :
                K[i][w] = 0
            elif valxpeso[i - 1][1] <= w and isNoOverlapped(pAnteri,pActual):
                    K[i][w] = max(valxpeso[i - 1][0] + K[i - 1][w - valxpeso[i - 1][1]], K[i - 1][w]) 
            else:
                K[i][w] = K[i - 1][w]
            
            # llena la Matriz alterna con la soluciones anteriores
            capsobrando = w
            solucion = []
            for j in range(i, 0, -1):
              #print(w,' ', i)
                if K[j][capsobrando] != K[j-1][capsobrando]:
                    solucion.append(j-1)
                    # solucion.append(M[j-1][0])
                    capsobrando = capsobrando - valxpeso[j-1][1]
                    S[i][w] = list(solucion)    

    capsobrando = capacidade
    escolhidos =[]
    #printMatriz(K)
    #printMatriz(S)

    for i in range(tamanho, 0, -1):
        #print(capsobrando,' ', i)
        if K[i][capsobrando] != K[i-1][capsobrando]:
            escolhidos.append(M[i-1][0])
            capsobrando = capsobrando - valxpeso[i-1][1]

    return escolhidos, (K[tamanho][capacidade])/2,'horas'

def leeArchivo():
    global archivo,entrada

    #src = 'C:\\Users\\kevin\\Desktop\\proyectoFinalFADA\\problema1Pd\\entradas\\punto1PdEntrada1.txt'
    src = 'C:\\Users\\kevin\\Desktop\\proyectoFinalFADA\\problema1Pd\\entradas\\punto1PdEntrada2.txt'
    #src = 'C:\\Users\\kevin\\Desktop\\proyectoFinalFADA\\problema1Pd\\entradas\\punto1PdEntrada3.txt'

    entrada = []
    archivo = open(src, 'r')
    n = archivo.readline()
    entrada = [None]*int(n)
    indice = 0

    for linea in archivo.readlines():
        entrada[indice]  = linea.split() # .split() convierte a una lista
        indice += 1
    archivo.close() 

    #printMatriz(entrada)

    
def printMatriz(a):
    #imprime una matriz
    print()
    for i in a:
        print(i)

def ordenarMatriz(a,colum):
    ##ordena una matriz de menor a mayor, recibe como argumentos una matriz 'a' y una columna 'colum', retorna una matriz ordena
    bco_x_des = sorted(a, key=itemgetter(colum-1))

    printMatriz(bco_x_des)
    return bco_x_des

def diferenciaHora(hIniStr, hFinStr):
    hIniDateObject = datetime.timedelta(hours= int(hIniStr[:hIniStr.find(':')]),minutes= int(hIniStr[hIniStr.find(':')+1:]))
    hFinDateObject = datetime.timedelta(hours= int(hFinStr[:hFinStr.find(':')]),minutes= int(hFinStr[hFinStr.find(':')+1:]))

    difHoraDateOnject = (hFinDateObject - hIniDateObject).total_seconds()

    difHora = difHoraDateOnject / 3600 # convierte el total de segundos a un numero decimal en horas
    #difMinutos = (difHoraDateOnject % 3600) //60

    #print('Diferencia hora: ', difHora)
    #print('Diferencia minutos', difMinutos)

    # El valor se multiplica por 2 para obtener una cantdad en fraciones de media hora (0.5) equivale a media hora, su nuevo valor 
    # sera (1), suponiendo que entra el valor (1.5 horas), su nuevo valor sera (3 "medias horas", que es lo mismo que tener 0.5 tres veces)
    difHora = difHora*2 

    return difHora

def strToDateObject(hora):
    hDateObject = datetime.datetime.strptime(hora, '%H:%M')
    return hDateObject 

def isNoOverlapped(hFin,hIni):
    h1 = strToDateObject(hFin)
    h2 = strToDateObject(hIni)
    #print('h1= ', h1, 'h2= ', h2)   
    
    if(h1 <= h2):
        return(True)   
    else: 
        return(False)

def valorPeso(a):
    lista1 = []
    for i in range(len(a)):
        valor =  diferenciaHora(a[i][1],a[i][2])
        #peso = 0
        lista1.append(list([int(valor), int(valor)]))
    #print(lista1)    
    return lista1

if __name__ == "__main__":
    # formato: valxpeso = [[valor, peso], ..., n]
    leeArchivo()
    matrizOrdenada = ordenarMatriz(entrada,2)
    
    valxpeso = valorPeso(matrizOrdenada)
    W = 48
    n = len(valxpeso)

    print('valorxpeso = ',valxpeso)
    #valorPeso(valxpeso)
    #valxpeso = [[8,8],[7,7],[11,11],[12,12],[2,2]]
    #imprime solucion
    print('Solucion: ',mochila(W, valxpeso, n, matrizOrdenada))
    
    #print(isNoOverlapped('13:00', '12:00'))