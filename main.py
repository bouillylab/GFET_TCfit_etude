import numpy as np
import matplotlib.pyplot as plt

# main.py Pas le bon nom

def csvRead(fichier, delimiter=",", skip_header=255, usecols=(1,2,3,4,5)) :
    data = np.genfromtxt(fichier, delimiter=",", skip_header=255, usecols=(1,2,3,4,5))

def XXXRead(fichier) :
    # lecture de fichier alternatif
    return None

def extractTC(fichier, fmt="stack", methode="csv") :

    data = csvRead(fichier) if methode=="csv" else 0
    Vg, time, I_s, I_d, I_g = data.T

    if fmt == "stack" :
        pass

def main(fichier) :
    #data = extractTC(fichier)
    data = np.genfromtxt(fichier, delimiter=",", skip_header=255, usecols=(1,2,3,4,5))
    Vg, time, I_s, I_d, I_g = data.T

    fig = plt.figure()
    axIs = fig.add_subplot()

    axIs.plot(Vg, I_s)

    fig = plt.figure()
    axVGT = fig.add_subplot(211)
    axIST = fig.add_subplot(212)

    axVGT.plot(time, Vg)
    axIST.plot(time, I_s)

    plt.show()

if __name__ == "__main__" :
    fichier = "data/data_PV/TC_good/I_V sweep LG mgf2_2_1.csv"
    main(fichier)
