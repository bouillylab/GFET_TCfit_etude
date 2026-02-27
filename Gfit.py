import numpy as np

from scipy.special import erf
from scipy.optimize import curve_fit, minimize  # rafinement avec minimize?

import math_utils as mu

## TODO
# et si la fonction est juste sigmoid ou juste erf?  Faux!!

def sigmoid(x, sigma, x0) :
    return 1 / (1 + np.exp( -(x - x0) * sigma ))

def erfFunc(x, A, sigma, x0) :
    return A * (erf((x - x0) * sigma) + 1) / 2

def branch(x, A, sigma1, x01, sigma2, x02) :
    return erfFunc(x, A, sigma1, x01) * sigmoid(x, sigma2, x02) 

def GFETFunc(x, A1, A2, sigma1, sigma2, x01, x02, ss1, ss2, S1, S2) :
    gauche = branch(x, A1, sigma1, x01, ss1, S1)
    droite = branch(x, A2, sigma2, x02, ss2, S2)

    return gauche + droite

def Gfit(x, y, maxfev=4000) :

    #CNP = np.argmin(y)

    #xG = x[:]

    popt, pcov = curve_fit(GFETFunc, x, y, maxfev=maxfev)

    return popt

def test(dossier) :

    A1 = 1
    A2 = 2
    sigma1 = 2
    sigma2 = -2
    x01 = 3
    x02 = 3
    ss1 = 2
    ss2 = -2
    S1 = 3
    S2 = 3

    x = np.linspace(-10, 10, 1000)

    y = erfFunc(x, A1, sigma1, x01)
    y2 = sigmoid(x, sigma1, x01)

    y3 = branch(x, A1, sigma1, x01, ss1, S1)
    y4 = branch(x, A2, sigma2, x02, ss2, S2)

    y5 = func(x, A1, A2, sigma1, sigma2, x01, x02, ss1, ss2, S1, S2)

    plt.plot(x, y5)
    plt.axhline(A1/2, ls=":", color="k")
    plt.axvline(x01, ls=":", color="k")

    #for data in dataMap :
    #    for Vg, time, Id, I_bin in data :
    #        plt.plot(Vg, Id)

    plt.show()

def test2(dossier) :
    def format(data) :
        Vg, time, Id, Is, Ig = data.T
        Id *= 1e5
        I_bin = np.array([Is, Ig])
        yield Vg, time, Id, I_bin

    def format2(data) :
        Vg, time, Id, Is, Ig = data.T

        Id *= 1e5

        Vg = np.reshape(Vg, shape=(2, -1))
        time = np.reshape(time, shape=(2, -1))
        Id = np.reshape(Id, shape=(2, -1))
        Is = np.reshape(Id, shape=(2, -1))
        Ig = np.reshape(Ig, shape=(2, -1))

        I_bin = np.array([Is, Ig])

        for i in range(2) :
            yield Vg[i], time[i], Id[i], I_bin[:, i]

    dataMap, nbrData = extractTC(dossier, fmt=format2)


    for data in dataMap :
        for Vg, time, Id, I_bin in data :
            popt = Gfit(Vg, Id, maxfev=100000)

            A1, A2,sigma1,sigma2,x01,x02,ss1,ss2,S1,S2  = popt

            plt.plot(Vg, GFETFunc(Vg, *popt), color="r")

            plt.plot(Vg,branch(Vg, A1, sigma1, x01, ss1, S1), ls=":")
            plt.plot(Vg,branch(Vg, A2, sigma2, x02, ss2, S2), ls=":")

            plt.plot(Vg, erfFunc(Vg, A1, sigma1,x01 ), ls="-.")
            plt.plot(Vg, erfFunc(Vg, A2, sigma2, x02 ), ls="-.")

            plt.plot(Vg, sigmoid(Vg, ss1,S1 ), ls="--")
            plt.plot(Vg, sigmoid(Vg, ss2,S2 ), ls="--")

            plt.plot(Vg, Id)
            plt.show()

if __name__ == "__main__" :
    import matplotlib.pyplot as plt
    from CSVRead import extractTC

    test2("data/data_PV/TC_good/")
