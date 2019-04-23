import random
import os

def generador(n):
    src = os.getcwd() #retorna la ruta actual de archivo .py
    archivoSalida = open(src + '\\pruebas.txt', 'w')
    archivoSalida.write(str(n) + '\n')
    print(n)
    for i in range(n):
        hI = random.randint(0,23)
        hF = 0
        while(hI > hF and hI != hF):
            hF = random.randint(0,24)

        if(hI< 10): hI = '0'+str(hI)     
        if(hF< 10): hF = '0'+str(hF)

        nom = 'Proc'+str(i+1)
        hhmmIni = str(hI)+':00'
        hhmmFin = str(hF)+':00'
        
        archivoSalida.write(nom+' '+hhmmIni+' '+hhmmFin+'\n')
        print(nom,hhmmIni,hhmmFin)
    archivoSalida.close()


if __name__ == "__main__":
    ent =input('digite una cantidad n:')
    generador(int(ent))