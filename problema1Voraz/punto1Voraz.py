from operator import itemgetter
from random import randint
import time
import datetime
import os
import shutil

def slectorActividades(n,c,f):
    
    s = []
    s.append(0) 
    k = 1
    z = 0

    for i in range(n):
        if(c[i] >= f[z]):
            s.append(i)  # actividad seleccionada
            z= i
            k += 1
    
    return s         

def nombresSolucion(nom, s):
    # nom = nombres de cada proceso
    # s = solucion de los proceso
    nomSol = []
    for i in range(len(s)):
        nomSol.append(nom[int(s[i] )])

    return nomSol

def toalHoras(b, s):
    # nom = nombres de cada proceso
    # s = solucion de los proceso
    total = []
    for i in range(len(s)):
        total.append(b[ int( s[i] ) ])

    return sum(total, 0)


def beneficio(n,c,f):
    # b = es el benefio, o la mejor dicho la diferencia en entre la hora de incio y la hora de finalzacion
    b = []
    for i in range(n):
        b.append(f[i]-c[i])    
    return b    

def horaToDecimal(hora):
    # Convierte una hora en formato (HH:MM) a un numero 
    hIniDateObject = datetime.timedelta(hours= int(hora[:hora.find(':')]),minutes= int(hora[hora.find(':')+1:]))
    decimalHora = hIniDateObject.total_seconds() / 3600
    return decimalHora     

def randomTime(start):
    h=randint(start,47)
    value =h/2
    if value==int(value):
        return str(int(value))+":00",h
    else:
        return str(int(value))+":30",h


def genMinutes(h):
    if h==24:
        return "00"
    if randint(0,1)==0:
        return "00"
    return "30"
    
def auxBegin(path):
    entrada = []
    archivoEntrada = open(path, 'r')
    n = archivoEntrada.readline()
    entrada = [None]*int(n)
    
    indice = 0
    for linea in archivoEntrada.readlines():
        entrada[indice]  = linea.split() # .split() convierte a una lista
        indice += 1
    archivoEntrada.close() 
    return n,entrada

def sortedProofs(matrix,files):
    shutil.rmtree("in",ignore_errors=True)
    shutil.rmtree("out",ignore_errors=True)
    os.makedirs(os.getcwd()+"/in")
    os.makedirs(os.getcwd()+"/out")
    i=1
    genProofs(files)
    time = open("timeSorted","w")
    while i<=files:
        n,entrada=auxBegin("/in"+str(files))
        startRunningTime = time.time()
        sorted(entrada,key=itemgetter(1))
        endRunningTime=time.time()-startRunningTime

        # se escribe el archivo de tiempos
        time.write(str(n)+":"+"{:1.5f}".format(endRunningTime)+"\n")
        i+=1
    time.close()


def begin(path):
    global entrada

    entrada = []
    archivoEntrada = open(path, 'r')
    n = archivoEntrada.readline()
    entrada = [None]*int(n)

    indice = 0
    for linea in archivoEntrada.readlines():
        entrada[indice]  = linea.split() # .split() convierte a una lista
        indice += 1
    archivoEntrada.close() 

    matrizOrdenada = sorted(entrada,key=itemgetter(1))
    # print(matrizOrdenada)
    nombres = []
    c = []
    f = []
    n = len(matrizOrdenada)
    for i in range(n):
        nombres.append(matrizOrdenada[i][0])
        c.append(horaToDecimal(matrizOrdenada[i][1]))
        f.append(horaToDecimal(matrizOrdenada[i][2]))
    # print('nombres = ', nombres)
    # print('c = ', c)
    # print('f = ', f) 
    # print()
    return nombres, c,f,n



def algo(nombres, c,f,n):
    """
    n = 5
    nombres = ['Proc1','Proc2','Proc3','Proc4','Proc5']

    s = [None]*50 #solucion
    c = [0,5,11,12,22] #comienzo de cada actividad
    f = [8,12,22,24,24] #finalizacion de cada actividad
    """

    b = beneficio(n,c,f) # beneficio
    solucion = slectorActividades(n,c,f)
    
    nProcedimientos = len(solucion)
    totalHoras = toalHoras(b,solucion)

    # print('Total horas = ', toalHoras(b,solucion))
    # print('Beneficio = ',b)
    # print('Indices de las solucion = ',solucion)
    # print('Nombres de la solucion = ',nombresSolucion(nombres,solucion))
    return nProcedimientos, totalHoras, nombresSolucion(nombres,solucion)

def writeFile(path,n, totalHoras, nombres):
    out = open(path,"w")
    out.write(str(n)+"\n")
    out.write(str(totalHoras)+"\n")
    i=0
    while i<n:
        out.write(nombres[i]+"\n")
        i+=1
    out.close()


def runAlgo(files):
    i=1
    timesFile = open("time","w")

    while i<=files:
        # se leen los datos
        startReadingTime = time.time()
        nombres, c,f,n = begin("in/in"+str(i))
        endReadingTime = time.time()-startReadingTime
        
        # se corre el algoritmo
        startTime = time.time()
        nProcedimientos, totalHoras, nombresSolucion=algo(nombres, c,f,n)
        endTime=time.time()-startTime
        

        # se escribe el archivo de repuesta
        startWrittingTime = time.time()
        writeFile("out/out"+str(i),nProcedimientos, totalHoras, nombresSolucion)
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

def genProofs(files):
    i=1
    while i<=files:
        # el factor de i especifica el salto entre la cantidad de 
        # procedimientos de cada archivo
        n = 10000*i
        file = open("in/in"+str(i),"w")
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

run(1)