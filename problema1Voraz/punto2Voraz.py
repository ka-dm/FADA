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




if __name__ == "__main__":
    n = 5
    nombres = ['Proc1','Proc2','Proc3','Proc4','Proc5']

    s = [None]*50 #solucion
    c = [0,5,11,12,22] #comienzo de cada actividad
    f = [8,12,22,24,24] #finalizacion de cada actividad
    
    b = beneficio(n,c,f) # beneficio
    solucion = slectorActividades(n,c,f)

    print('Total horas = ', toalHoras(b,solucion))
    print('Beneficio = ',b)
    print('Indices de las solucion = ',solucion)
    print('Nombres de la solucion = ',nombresSolucion(nombres,solucion))
    