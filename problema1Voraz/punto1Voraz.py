from operator import itemgetter
import datetime
import os

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

def leeArchivo(rutaArchivo):
    global entrada
    
    #src = 'C:\\Users\\kevin\\Desktop\\proyectoFinalFADA\\problema1Pd\\entradas\\punto1PdEntrada1.txt'

    src = rutaArchivo

    entrada = []
    archivoEntrada = open(src, 'r')
    n = archivoEntrada.readline()
    entrada = [None]*int(n)
    indice = 0

    for linea in archivoEntrada.readlines():
        entrada[indice]  = linea.split() # .split() convierte a una lista
        indice += 1
    archivoEntrada.close() 

    #printMatriz(entrada)

def crearArchivoSalida(totalH,contenido):
    src = os.getcwd() #retorna la ruta actual de archivo .py

    archivoSalida = open(src + '\\punto1VorazSalida.txt', 'w')
    archivoSalida.write(str(totalH) + '\n')
    for i in range(len(contenido)):
        archivoSalida.write(str(contenido[i]) + '\n')
    archivoSalida.close()

    print("#################################################")
    print("# Se genero correctamente el archivo de salida. #")
    print("#################################################")    

def printMatriz(a):
    #imprime una matriz
    print()
    for i in a:
        print(i)
    print()    

def ordenarMatriz(a,colum):
    ##ordena una matriz de menor a mayor, recibe como argumentos una matriz 'a' y una columna 'colum', retorna una matriz ordena
    bco_x_des = sorted(a, key=itemgetter(colum-1))
    #printMatriz(bco_x_des)
    return bco_x_des

def horaToDecimal(hora):
    # Convierte una hora en formato (HH:MM) a un numero 
    hIniDateObject = datetime.timedelta(hours= int(hora[:hora.find(':')]),minutes= int(hora[hora.find(':')+1:]))
    decimalHora = hIniDateObject.total_seconds() / 3600
    return decimalHora     


if __name__ == "__main__":
    src = input("Ingrese la ruta del archivo: ")
    #src = 'C:\\Users\\kevin\\Desktop\\proyectoFinalFADA\\problema1Pd\\entradas\\punto1PdEntrada3.txt'
    leeArchivo(src)
    matrizOrdenada = ordenarMatriz(entrada,2)
    #printMatriz(matrizOrdenada)

# --------------------- Extrae los los arrays corespondientes de la matriz ordenada ------------------------------
    nombres = []
    c = []
    f = []
    n = len(matrizOrdenada)
    for i in range(n):
        nombres.append(matrizOrdenada[i][0])
        c.append(horaToDecimal(matrizOrdenada[i][1]))
        f.append(horaToDecimal(matrizOrdenada[i][2]))
    #print('nombres = ', nombres)
    #print('c = ', c)
    #print('f = ', f) 
    #print()
#-----------------------------------------------------------------------------------------------------------------    
    """
    n = 5
    nombres = ['Proc1','Proc2','Proc3','Proc4','Proc5']

    s = [None]*50 #solucion
    c = [0,5,11,12,22] #comienzo de cada actividad
    f = [8,12,22,24,24] #finalizacion de cada actividad
    """
# --------------------- Imprime la solucion del problema ------------------------------    
    #"""
    b = beneficio(n,c,f) # beneficio
    solucion = slectorActividades(n,c,f)
    totalH = toalHoras(b,solucion)
    nombreSol = nombresSolucion(nombres,solucion)

    crearArchivoSalida(totalH,nombreSol)

    print('Total horas = ', totalH)
    print('Beneficio = ',b)
    print('Indices de las solucion = ',solucion)
    print('Nombres de la solucion = ',nombreSol)
    #"""
#-----------------------------------------------------------------------------------------------------------------        