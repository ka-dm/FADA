##########################################{ Declaracion }##########################################
from operator import itemgetter
import datetime
import os
from random import randint
import time
import shutil
from tqdm import tqdm

def usoSalaCirugias(entrada):
    """
    Este algoritmo recibe los siguientes parametros:
        cap = es la capacida maxima
        beneficio = es una matriz 2*n, que contiene un valor y un peso asociado a cada proceso
        M = es una matriz matriz ordenada por la hora de incio, la cual contiene la informacion leida del archivo de entrada de cada proceso
    """
    M = ordenarMatriz(entrada,2)
    beneficio = valorPeso(M)
    cap = 48

    n = len(beneficio)
    K = [[0 for x in range(cap+1)] for x in range(n+1)] #Crea y llena la matriz con 0's
    S = [[None for x in range(cap+1)] for x in range(n+1)] #Crea y llena la matriz con None
    
    for i in range(n + 1):
        for w in range(cap + 1):
            
            indiceAnt = str(S[i-1][w])
            indiceAnt = (indiceAnt.replace('[','').replace(']','')).split(',')  # Elimina los caracteres indicados, y convierte el str a una lista
            procAct = M[i-1][1] 
            if indiceAnt[0] != 'None': procAnt = M[int(indiceAnt[0])][2] # Si el indice anterior es vacio, establece una hora predeterminada
            else: procAnt = '00:00'

            # llena y verifica que no esten solapados dos procesos
            if i == 0 or w == 0 :
                K[i][w] = 0
            elif beneficio[i - 1][1] <= w and noEstaSolapado(procAnt,procAct):
                K[i][w] = max(beneficio[i - 1][0] + K[i - 1][w - beneficio[i - 1][1]], K[i - 1][w]) 
            else:
                K[i][w] = K[i - 1][w]
            
            # llena la Matriz alterna con la soluciones anteriores
            capSobrante = w
            solucion = []
            for k in (range(i, 0, -1)):
              #print(w,' ', i)
                if K[k][capSobrante] != K[k-1][capSobrante]:
                    solucion.append(k-1)
                    # solucion.append(M[k-1][0])
                    capSobrante = capSobrante - beneficio[k-1][1]
                    S[i][w] = list(solucion)  
    
    procEscogidos =[]
    for i in range(len(S[n][w])):
        procEscogidos.append(M[S[n][w][i]][0]) # Busca los nombres de los procedimientos en la matriz M, y los agrega en una lista. 

    return procEscogidos, (K[n][cap])/2,'horas'




def begin(path):
    entrada = []
    archivoEntrada = open(path, 'r')
    n = int(archivoEntrada.readline())
    entrada = [None]*int(n)
    indice = 0

    for linea in archivoEntrada.readlines():
        entrada[indice]  = linea.split() # .split() convierte a una lista
        indice += 1
    archivoEntrada.close() 
    return entrada,n

def writeFile(path,proc):
    archivoSalida = open(path, 'w')
    archivoSalida.write(str(proc[1]) + '\n')
    for i in range(len(proc[0])):
        archivoSalida.write(str(proc[0][i]) + '\n')
    archivoSalida.close()

def ordenarMatriz(a,colum):
    ##ordena una matriz de menor a mayor, recibe como argumentos una matriz 'a' y una columna 'colum', retorna una matriz ordena
    bco_x_des = sorted(a, key=itemgetter(colum-1))
    #printMatriz(bco_x_des)
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

def noEstaSolapado(hFin,hIni): 
    # Compara la hora de finalizacion con la hora de incio entre dos procesos 
    h1 = horaToDecimal( hFin) * 2
    h2 = horaToDecimal( hIni) * 2
    if(h1 <= h2):
        return(True)   
    else:
        return(False)

def horaToDecimal(hora):
    # Convierte una hora en formato (HH:MM) a un numero 
    hIniDateObject = datetime.timedelta(hours= int(hora[:hora.find(':')]),minutes= int(hora[hora.find(':')+1:]))
    decimalHora = hIniDateObject.total_seconds() / 3600
    return decimalHora        

def valorPeso(a):
    lista1 = []
    for i in range(len(a)):
        valor =  diferenciaHora(a[i][1],a[i][2])
        #peso = 0
        lista1.append(list([int(valor), int(valor)]))
    #print(lista1)    
    return lista1

def randomTime(start):
    h=randint(start,47)
    value =h/2
    if value==int(value):
        return str(int(value))+":00",h
    else:
        return str(int(value))+":30",h


def runAlgo(files):
    print("--------------------[         Corriendo pruebas       ]--------------------")
    timesFile = open("time","w")

    for i in tqdm(range(files)):
        # se leen los datos
        startReadingTime = time.time()
        entrada,n= begin("in/in"+str(i+1))
        endReadingTime = time.time()-startReadingTime
        
        # se corre el algoritmo
        startTime = time.time()
        proc=usoSalaCirugias(entrada)
        endTime=time.time()-startTime
        

        # se escribe el archivo de repuesta
        startWrittingTime = time.time()
        writeFile("out/out"+str(i+1),proc)
        endWrittingTime=time.time()-startWrittingTime

        # se escribe el archivo de tiempos
        timesFile.write(str(n)+":"+"{:1.5f}".format(endTime)+":"+"{:1.5f}".format(endReadingTime)+":"+"{:1.5f}".format(endWrittingTime)+"\n")
        i+=1
    
    timesFile.close()


def run(files):
    # se eliminan las carpetas con las pruebas anteriores
    shutil.rmtree("in",ignore_errors=True)
    shutil.rmtree("out",ignore_errors=True)
    # se recrean las carpetas para pruebas
    os.makedirs(os.getcwd()+"/in")
    os.makedirs(os.getcwd()+"/out")
    # se generan las pruebas
    genProofs(files)
    # se generan las salidas
    runAlgo(files)  
    print("--------------------[ Pruebas terminadas correctamente ]--------------------")
    

def genProofs(files):
    print("--------------------[          Generando pruebas       ]--------------------")
    for i in tqdm(range(files)):
        # el factor de i especifica el salto entre la cantidad de 
        # procedimientos de cada archivo
        n = 10*(i+1)
        file = open("in/in"+str(i+1),"w")
        file.write(str(n)+"\n")
        j=1
        while j<=n:
            hString, h = randomTime(0)
            file.write("proc"+str(j)+" "+hString+" ")
            hString, h = randomTime(h)
            file.write(hString+"\n")
            j+=1
        i+=1
    file.close()

##########################################{ Ejecucion }##########################################
os.system("pip install tqdm")
run(10)