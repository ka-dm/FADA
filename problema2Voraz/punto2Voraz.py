##########################################{ Introduccion }##########################################

#Condiciones iniciales
# Se cosidera para el desarrollo del algoritmo que el orden o secuencia que tienen
# los libros no se puede alterar dado que en la salida lo unico que puede especificarse
# son las distribuciones de libros a los n autores y el tiempo total de copiado
# segun lo que dice el el siguiente fragmento "y cada una las n líneas siguientes 
# represente la distribución de libros elegida, indicando para cada escritor desde y 
# hasta qué libro va a copiar"
# Se entiende por distribución a la asignación de libros a los escritores,
# de modo que [1-1][2-3][4-6][7-7] podria ser una distribucion de siete(7) libros a
# cuatro(4) escritores y [1-1][2-2][3-3][4-7] es otra distribución de esos mismos
# siete(7) libros a los mismos cuatro(4) escritores, que representa una distribucion
# diferente a la anterior pero conserva el mismo orden iniciar donde el primer libro
# ocupa la misma posicion en ambas secuencias, el segundo libro ocupa la misma posición
# en ambas secuencias, el tercero libro ocupa la misma posición en ambas secuencias y así
# sucesivamente

##Pruebas de Escritorio
##Prueba 1
# "Grupo ideal para un total de 360 paginas y 5 escritores"
# [72,72,72,72,72,72,72,72,72,72], n=5

# "Grupo actual"
# [li1,li2,li3,li4,li5,li6,li7,li8,li9,li10]
# [10,10,10,10,80,10,200,10,10,10]


# "Ideal 72*"
# {[1-4]}=40 (72-40=32) vs [1-5]=120 (120-72=48)
# [5-*]=0 (∞) vs {[5-5]}=80 (80-72=8)
# {[6-6]}=10 (72-10=62) vs [6-7]=210 (210-72=138)
# [7-*]=0 (∞) vs {[7-7]}=200 (200-72=148)
# [8-10]=30

# 200
# [01-04] -> 40
# [05-05] -> 80
# [06-06] -> 10
# [07-07] -> 200
# [08-10] -> 30

# ##Prueba 2
# [15,47,36,41,62];n=3

# "Ideal 67*"
# {[1,2]}=62 (67-62)=5 vs [1,3]=98 (98-76)=22
# [3,3]=36 (67-36)=31 vs {[3,4]}=77 (77-67)=10
# {[5,5]}=62

# 67
# [01-02] -> 62
# [03-04] -> 77
# [05-05] -> 62

# ##Prueba 3
# [15,47,36,41,62];n=4
# [2,3]

# "Ideal 50,25*"
# [1,1]=15 vs {[1,2]=62}
# {[3,3]=36} vs [3,4]=77
# {[4,4]=41} vs [4,5]=103
# {[5,5]=62}

# 50,25
# [01-02] -> 62
# [03-03] -> 36
# [04-04] -> 41
# [05-05] -> 62

##########################################{ Declaracion }##########################################
# para generar numeros aleatorios
# para las pruebas
from random import randint
# para editar (borrar/crear) las carpetas que
# contienen los archivos de las pruebas
import os
import shutil
# para hacer el calculo en el tiempo de ejecución
import time


#Inicia tomando un archivo y recuperando la informacion para ser procesado
# --- [entras] ---
# path: String que contiene la ruta relativa del archivo
# que se leerá
# --- [salidas] ---
# m: la cantidad de libros del archivo path
# n: la cantidad de escritores en el archivo path
# p: la lista con las cantidades de paginas de los libros
# ideal: el promedio de paginas por escritor
def begin(path):
    #Se abre el arhivo
    archivo = open(path)
    nm = archivo.readline()
    #se capturan los valores de escritores y libros
    n = int(nm.split()[0])
    m = int(nm.split()[1])
    names = []
    p = []
    # se capturan las cantidades de páginas y los nombres
    for linea in archivo.readlines():
        names.append(linea.split()[0])
        p.append(linea.split()[1])
    p = list(map(int,p))
    # se calcula el promedio de páginas por escritor
    # que será usado mas adelante para saber si un libro
    # debe o no asignarse a un escritor
    ideal = sum(p,0)/n
    # se retornan todos los datos obtenidos excepto la lista de nombres 
    # ya que no es usada
    return m,n,p,ideal

# Es el procedimiento que se encarga de encontrar la forma de
# distribuir los libros a los escritores
# --- [entras] ---
# m: la cantidad de libros de la entrada
# n: la cantidad de escritores de la entrada
# p: la lista con las cantidades de paginas de la entrada
# ideal: el promedio de paginas por escritor
# --- [salidas] ---
# out: el arreglo con las posiciones de marcación de asignacion de libros
# max: el acumulado maximo de paginas en la asignacion (tiempo total de duracion de copiado)
def algo(m,n,p,ideal):
    # i: el indice que itera la lista de numero de páginas
    i=0
    # j: indice para llevar conteo de escritores
    j=0
    # impresión para hacer verificaciones
    #print("m:"+str(m))
    #print("n:"+str(n))
    # max: variable que guarda el valor que se tardará en
    # transcribir la obra completa
    max=0
    # carry: guarda el acumulado de paginas que tiene un lector,
    # es reutilizada para cada lector, es decir, se 
    # vacea cada vez que se le asignaran libros a otro lector
    carry=0
    # out: arreglo de numeros con las posiciones para "partir" el
    # arreglo p, ej: sea p=[14,5,16,20,8] y n=3 es decir, hay 5 libros
    # y 3 autores, si out=[2,4] se dice que la distribución de libros 
    # para los autores deberia ser [1,2][3,4][4,5] luego se entiende
    # que la cardinalidad de out deberia ser siempre n-1
    out = []
    # se descarta el caso trivial para max, si hay un solo autor
    # el/las tiempo/paginas total(es) es la suma de los tiempos/paginas
    # de todos los libros
    if n==1:
        max=sum(p)
    # Si hay mas de un escritor
    if 1<n:
        # si hay menos libros que escritores el problema no tiene mucho sentido
        # pues solamente se debe asignar un libro a cada escritor
        if m<=n:
            # se itera conforme a la cantidad de libros
            while i<m:
                # se empieza la busqueda del libro mas largo
                # comparando el valor de paginas del libro
                # actual con el anterior
                if max<p[i]:
                    max=p[i]
                # se agregan las posiciones en las que se "parte"
                # el arreglo
                out.append(i)
                i+=1
        # el problema tiene mas sentido cuando hay mas libros que escritores
        # porque es necesario hacer una buena distribución
        else:
            # se itera conforme a la cantidad de libros para
            while i<m:
                # si no se tienen paginas acumuladas para
                # un lector entonces se asignan las del libro actual
                if carry==0:
                    carry+=p[i]
                    # se compara si es el acumulado de paginas mas largo
                    if max<carry:
                        max=carry
                    i+=1
                # si ya se ha asignado un numero de paginas previamente al escritor
                else:
                    # se pregunta si asignado las paginas del libro actual
                    # el autor sobrepasa el numero de paginas promedio
                    if ideal<carry+p[i]:
                        # si asignando el libro actual el numero de paginas promedio es sobrepasado
                        # se toma la mejor decision teniendo en cuenta el numero de paginas que menos 
                        # se aleje del promedio
                        if aux(carry,p[i],ideal):
                            # el libro no pudo ser asignado porque el numero de paginas se alejó
                            # mas del promedio asignandolo
                            
                            # se borra la variable de paginas acumuladas para
                            # la proxima asginación
                            carry=0
                            # se itera solamente hasta el siguiente escritor
                            j+=1
                            # se agrega el marcador de posicion hasta el libro actual
                            out.append(i)

                        # si el libro es asignado 
                        else:
                            # se agrega el numero de paginas del libro actual al acumulado
                            carry += p[i]
                            # se actualiza el numero maximo de paginas acumuladas
                            if max<carry:
                                max=carry
                            # se restaura el numero de paginas acumuladas
                            carry=0
                            # se da paso al siguiente libro y al siguiente escritor
                            i+=1
                            j+=1
                            # se agrega el marcador de posición hasta el libro actual
                            out.append(i)
                    
                    # si asignando el libro actual no se sobrepasa el numero de paginas
                    # promedio por escritor, el libro se asignará
                    else:
                        # se agrega el numero de paginas del libro actual al acumulado
                        carry += p[i]
                        # se actualiza el acumulado maximo
                        if max<carry:
                            max=carry
                        # se da paso al siguiente libro
                        i+=1

    # se retorna el arreglo con las posiciones de marcación y el acumulado maximo de paginas 
    # para un escritor
    return out,max

# Es el procedimiento que se encarga de decidir si
# será asignado o no un libro segun su numero de paginas,
# el acumulado de paginas actual para el escritor y
# el promedio de paginas por escritor
# --- [entras] ---
# carry: el numero de paginas acumuladas hasta el momento de la
# asignación
# p: el numero de páginas del libro a comparar
# ideal: el promedio de paginas por escritor
# --- [salidas] ---
# Boolean: true si el libro no seberia ser asignado false en caso contrario

def aux(carry,p,ideal):
    noAsignado = ideal-carry
    asignado = (carry+p)-ideal
    if(noAsignado<asignado):
        return True
    return False

# Prepara un arreglo a partir del las marcas de posicion
# de las asignaciones de libros
# --- [entras] ---
# m: la cantidad de libros
# n: el numero de escritores
# out: es una arreglo numerico que contiene 
# la salida de algo() con las marcas de posición
# de las asignaciones de libros
# --- [salidas] ---
# printable: una lista "imprimible" para mostrar
# las asignaciones de libros a los escritores con m*2 elementos
# en caso de que n=1 , contiene 2 elementos [1,m] resolviendo
# el caso trivial donde solo hay un escritor
def prepare(m,n,out):
    i=0
    printable =[]
    # si el arreglo out[] esta vacio es porque
    # solamente habia un escritor
    if len(out)==0:
        printable.append(1)
        printable.append(m)
    else:
        # si hay mas de un escritor
        while i<len(out):
            if i==0:
                # si hay solo dos escritores
                if len(out)==1:
                    printable.append(1)
                    printable.append(out[i])
                    printable.append(out[i]+1)
                    printable.append(m)
                    i+=1
                # en caso de que hayan mas escritores
                else:
                    # se incluye el índice del primer libro asginado (1)
                    printable.append(1)
                    # se incluye el índice el primer marcador (ya que i==0)
                    printable.append(out[i])
                    i+=1
            
            # si no se está procesando el primer marcador
            else:
                # se verifica si es el ultimo marcador
                if i==len(out)-1:
                    # si el marcador esta despues del ultimo libro
                    if out[i]==m:
                        # se incluye el marcador posterior del libro anterior
                        printable.append(out[i-1]+1)
                        # el marcador final (tambien m)
                        printable.append(out[i])
                        # y se termina el while
                        i+=1

                    # si es el ultimo marcador y no está despues del ultimo libro
                    else:
                        # se incluye el marcador posterior del libro anterior
                        printable.append(out[i-1]+1)
                        # el marcador actual
                        printable.append(out[i])
                        # el siguiente marcador
                        printable.append(out[i]+1)
                        # y el marcador final
                        printable.append(m)
                        # y se termina el while
                        i+=1
                
                # si el marcador representa una posición intermedia
                else:
                    # se incluye el marcador posterior del libro anterior
                    printable.append(out[i-1]+1)
                    # y el marcador siguiente
                    printable.append(out[i])
                    i+=1    
    
    # este es un ajuste final en caso de que hayan menos libros que escritores
    if m<=n:
        return printable[2:]
    else:
        return printable

# Procedimiento encargado de escribir los datos
# de una respuesta a un archivo de texto
# --- [entras] ---
# array: es el arreglo "printable" de la salida de
# la funcion prepare()
# duration: es la duración de copiado de la obra 
# (anteriormente llamado "max" en algo())
# path: String con ruta y nombre del archivo para escribir
# --- [salidas] ---
# none
def writeFile(array,duration,path):
    out = open(path,"w")
    m=len(array)
    out.write(str(duration)+"\n")
    i=0
    while i<m:
        out.write("["+str(array[i])+"-"+str(array[i+1])+"]"+"\n")
        i+=2
    out.close()

# Corre las pruebas que se encuentran en la carpeta "in" y 
# escribe sus salidas en la carpeta "out" ademas escribe un arhivo
# con los tiempos de ejecucion de las pruebas
# --- [entras] ---
# files: el numero de pruebas/archivos que se crearán/resolverán
# --- [salidas] ---
# none
def runAlgo(files):
    i=1
    timesFile = open("time","w")
    while i<=files:
        # se llama a begin() para capturar los datos del archivo
        
        startReadingTime = time.time()
        m,n,p,ideal = begin("in/in"+str(i))
        endReadingTime = time.time()-startReadingTime
        
        # se corre el algoritmo
        startTime = time.time()
        out,duration = algo(m,n,p,ideal)
        endTime=time.time()-startTime
        
        
        # cuestiones de verificación
        #print(p)
        #print(out)

        # se escribe el archivo de repuesta
        startWrittingTime = time.time()
        writeFile(prepare(m,n,out),duration,"out/out"+str(i))
        endWrittingTime=time.time()-startWrittingTime

        # se escribe el archivo de tiempos
        timesFile.write(str(m)+":"+"{:1.5f}".format(endTime)+":"+"{:1.5f}".format(endReadingTime)+":"+"{:1.5f}".format(endWrittingTime)+"\n")
        i+=1
    
    timesFile.close()

# Orquesta la generación de pruebas y la resolución de estas
# --- [entras] ---
# files: el numero de pruebas/archivos que se crearán/resolverán
# --- [salidas] ---
# "se deben revisar los archivos en las carpetas "in" y "out" para comprobar
# las pruebas"
def run(files):
    # se eliminan las carpetas con las pruebas anteriores
    shutil.rmtree("in",ignore_errors=True)
    shutil.rmtree("out",ignore_errors=True)
    # se recrean las carpetas para pruebas
    os.makedirs(os.getcwd()+"/in")
    os.makedirs(os.getcwd()+"/out")
    # se generan las pruebas
    genProofs(1000,10,files,7)
    # se generan las salidas
    runAlgo(files)     

# Generador de pruebas para el algortimo a partir de valores
# aleatorios
# --- [entras] ---
# pagesLimit: el numero maximo de paginas para un libro
# writersLimit: el numero maximo de escritores en cada problema
# files: el numero de archivos aleatorios de pruebas para generar
# booksLimit: el numero maximo de libros para asignar en cada problema
# --- [salidas] ---
# none
def genProofs(pagesLimit,writersLimit,files,booksLimit):
    i=1
    while i<=files:
        #n = randint(1,writersLimit)
        # ajuste manual de numero de escritores
        n = 5
        
        #m = randint(writersLimit,booksLimit)
        # ajuste progresivo del numero de libros
        m = 10*i
        # se usa la carpeta "in" para depositar los problemas
        file = open("in/in"+str(i),"w")
        file.write(str(n)+" ")
        file.write(str(m)+"\n")
        j=1
        while j<=m:
            file.write("libro"+str(j)+" "+str(randint(1,pagesLimit))+"\n")
            j+=1
        i+=1
    file.close()

##########################################{ Ejecucion }##########################################
run(1)

