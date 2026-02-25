import numpy as np
import matplotlib.pyplot as plt

from scipy.special import erf
from scipy.optimize import curve_fit
# main.py Pas le bon nom

def sigmoid(x, sigma, s) :
    return 1 / (1 + np.exp((-x + s)*sigma))

def erfS(x, A, sigma, s) :
    return A * ( erf((x - s)*sigma) + 1 )/2

def TC(x, A1, A2, sigma1, sigma2, s1, s2, ss1, ss2, S1, S2) :
    """
    A1, A2 : amplitude des deux erf
    sigma1, sigma2 : pente des erf
    s1, s2 : x0 des deux erf

    ss1, ss2 : sigma des sigmoid
    S1, S2 : x0 des sigmoid

    """
    sig1 = sigmoid(x, ss1, S1)
    sig2 = sigmoid(x, ss2, S2)

    erf1 = erfS(-x, A1, sigma1, -s1) * (1-sig1)
    erf2 = erfS(x, A2, sigma2, s2) * sig2
    #erf1 = A1 * (erf( (-x + s1 )*sigma1) + 1) / 2 * (1-sig1)
    #erf2 = A2 * (erf((x - s2)*sigma2) + 1) / 2 * sig2

    return erf1  + erf2 

def csvRead(fichier, delimiter=",", skip_header=255, usecols=(1,2,3,4,5)) :
    data = np.genfromtxt(fichier, delimiter=",", skip_header=255, usecols=(1,2,3,4,5))

    return data

def XXXRead(fichier) :
    # lecture de fichier alternatif
    return None

def extractTC(fichier, fmt="stack", methode="csv") :

    data = csvRead(fichier) if methode=="csv" else 0
    Vg, time, Is, Id, Ig = data.T

    if fmt == "stack" : # prend pour acquis que le data est symétrique 
        Vg = np.reshape(Vg, shape=(2, -1))
        time = np.reshape(time, shape=(2, -1))
        Is = np.reshape(Is, shape=(2, -1))
        Id = np.reshape(Id, shape=(2, -1))
        Ig = np.reshape(Ig, shape=(2, -1))

    #dataWrap = zip(Vg, Is, Id, Ig)
    dataWrap = np.array([Vg, Is, Id, Ig])
    return dataWrap, time

def main(fichier) :
    data, time = extractTC(fichier, fmt="stack")
    Vg, Id, Is, Ig = data[:,0]

    Id *= 1e5

    erfSig_g = lambda x, A, sig, s, ss, S : erfS(-x, A, sig, s) * (1-sigmoid(x, ss, S))
    erfSig_d = lambda x, A, sig, s, ss, S : erfS(x, A, sig, s) * (sigmoid(x, ss, S))

    minn = np.argmin(Id)

    Vg_g = Vg[:minn]
    Vg_d = Vg[minn:]

    Id_g = Id[:minn]
    Id_d = Id[minn:]

    poptG,_ = curve_fit(erfSig_g, Vg_g, Id_g, maxfev=40000)
    poptD,_ = curve_fit(erfSig_d, Vg_d, Id_d, maxfev=40000)
    A1, sig1, s1, ss1, S1 = poptG
    A2, sig2, s2, ss2, S2 = poptD

    P0 = np.array([A1,A2, sig1, sig2, s1, s2, ss1, ss2, S1, S2])
    popt, pcov = curve_fit(TC, Vg, Id, p0 = P0, maxfev=40000)

    A1, A2, sigma1, sigma2, s1, s2, ss1, ss2, S1, S2 = popt
    e1 = erfS(-Vg, A1, sigma1, -s1)
    e2 = erfS(Vg, A2, sigma2, s2)

    sig1 = 1 - sigmoid(Vg, ss1, S1)
    sig2 = sigmoid(Vg, ss2, S2)


    fig = plt.figure()
    ax = fig.add_subplot()

    ax.scatter(Vg, Id, s=5)
    #ax.plot(Vg_g, Id_g)
    #ax.plot(Vg_d, Id_d)
    ax.plot(Vg, TC(Vg, *popt), color="r")
    ax.plot(Vg, e1 * sig1, ls=":", label="erf1")
    ax.plot(Vg, e2 * sig2, ls=":", label="erf2")

    #ax.plot(Vg, erfSig_g(Vg, *poptG), ls="--")
    #ax.plot(Vg, erfSig_d(Vg, *poptD), ls="--")

    ax.scatter(Vg[minn], Id[minn])

    plt.show()

if __name__ == "__main__" :
    fichier = "data/data_PV/TC_good/I_V sweep LG mgf2_2_2.csv"
    main(fichier)

