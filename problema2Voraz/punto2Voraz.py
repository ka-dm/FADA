#####################{ Pruebas }#####################

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

#####################{ Declaracion }#####################

from random import randint
import os
import shutil

def begin(path):
    archivo = open(path)
    nm = archivo.readline()
    n = int(nm.split()[0])
    m = int(nm.split()[1])
    names = []
    p = []
    for linea in archivo.readlines():
        names.append(linea.split()[0])
        p.append(linea.split()[1])
    p = list(map(int,p))
    ideal = sum(p,0)/n
    return m,n,p,ideal

def algo(m,n,p,ideal):
    i=0
    j=0
    print("m:"+str(m))
    print("n:"+str(n))
    max=0
    carry=0
    out = []
    if n==1:
        max=sum(p)
    if 1<n:
        if m<=n:
            while i<m:
                if i==0:
                    max=p[i]
                if max<p[i]:
                    max=p[i]
                out.append(i)
                i+=1
        else:
            while i<m:
                if carry==0:
                    carry+=p[i]
                    if max<carry:
                        max=carry
                    i+=1
                else:
                    if ideal<carry+p[i]:
                        if aux(carry,p[i],ideal):
                            if max<carry:
                                max=carry
                            carry=0
                            j+=1
                            out.append(i)

                        else:
                            carry += p[i]
                            if max<carry:
                                max=carry
                            carry=0
                            i+=1
                            j+=1
                            out.append(i)
                    else:
                        carry += p[i]
                        if max<carry:
                            max=carry
                        i+=1
    return out,max

def aux(carry,p,ideal):
    before = ideal-carry
    after = (carry+p)-ideal
    if(before<after):
        return True
    return False


def prepare(m,n,out):
    i=0
    printable =[]
    if len(out)==0:
        printable.append(1)
        printable.append(m)
    else:
        while i<len(out):
            if i==0:
                if len(out)==1:
                    printable.append(1)
                    printable.append(out[i])
                    printable.append(out[i]+1)
                    printable.append(m)
                    i+=1
                else:
                    printable.append(1)
                    printable.append(out[i])
                    i+=1
            else:
                if i==len(out)-1:
                    if out[i]==m:
                        printable.append(out[i-1]+1)
                        printable.append(out[i])
                        i+=1
                    else:
                        printable.append(out[i-1]+1)
                        printable.append(out[i])
                        printable.append(out[i]+1)
                        printable.append(m)
                        i+=1
                else:
                    printable.append(out[i-1]+1)
                    printable.append(out[i])
                    i+=1    
    if m<=n:
        return printable[2:]
    else:
        return printable

def writeFile(array,duration,path):
    out = open(path,"w")
    m=len(array)
    out.write(str(duration)+"\n")
    i=0
    while i<m:
        out.write("["+str(array[i])+"-"+str(array[i+1])+"]"+"\n")
        i+=2
    out.close()

def genProofs(pagesLimit,writersLimit,filesLimit,booksLimit):
    i=1
    while i<=filesLimit:
        n = randint(1,writersLimit)
        m = randint(writersLimit,booksLimit)
        file = open("in/in"+str(i),"w")
        file.write(str(n)+" ")
        file.write(str(m)+"\n")
        j=1
        while j<=m:
            file.write("libro"+str(j)+" "+str(randint(1,pagesLimit))+"\n")
            j+=1
        i+=1
    file.close()

def runAlgo(filesLimit):
    i=1
    while i<=filesLimit:
        m,n,p,ideal = begin("in/in"+str(i))
        out,duration = algo(m,n,p,ideal)
        print(p)
        print(out)
        writeFile(prepare(m,n,out),duration,"out/out"+str(i))
        i+=1

def run(filesLimit):
    shutil.rmtree("in",ignore_errors=True)
    shutil.rmtree("out",ignore_errors=True)
    os.makedirs(os.getcwd()+"/in")
    os.makedirs(os.getcwd()+"/out")
    genProofs(20,5,filesLimit,7)
    runAlgo(filesLimit)     

#####################{ Ejecucion }#####################
run(1)






