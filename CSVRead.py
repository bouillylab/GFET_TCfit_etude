import sys, os
import numpy as np

def csvRead(fichier, delimiter, skip_header, usecols) :
    """
    - retourne le data du fichier CSV demandé

    arguments :
        - string fichier : fichier.csv
        - string delimiter : ce qui séparer une case du csv
        - int skip_header : nbr de ligne à sauter
        - tuple usecols : colones à utilisé

    return :
        - array (N, M) data N colones M valeurs
    """
    data = np.genfromtxt(fichier, delimiter=delimiter, skip_header=skip_header, usecols=usecols)

    return data

def extractTC(dossier, fmt=None, delimiter=",", skip_header=255, usecols=(1,2,3,4,5)) :
    """
    - retoune les TC des fichiers .csv contenu dans un dossier

    arguments :
        - string dossier : dossier avec les csv
        - func fmt = None : fonction servant au formatage
        - string delimiter = "," : ce qui sépare une case
        - int skip_header = 255 : lignes à sauté
        - tuple usecols = (1,2,3,4,5) : colones à utilisé

    return :
        - map dataMap : map des data formaté selon fmt, generator
        - int nbrFichier : nbr de fichier dans le dossier donné

    """


    pathToFichier = lambda fichier : f"{dossier}/{fichier}"
    csvReadP = lambda fichiers : csvRead(fichiers, delimiter, skip_header, usecols)

    def dataRaw(data) :
        """
        fonction interne, na pas utilisé

        formatage None, retourne le data comme tel
        """
        Vg, time, Id, Is, Ig = data.T
        I_bin = np.array([Is, Ig])
        yield Vg, time, Id, I_bin

    nbrFichier = len(os.listdir(dossier))
    fichiers = map(pathToFichier, os.listdir(dossier))  # chemin vers chaque fichier, pas encore ouvert
    dataMap = map(csvReadP, fichiers)   # ouvre les fichier juste quand call, mais après ne le ferme pas?

    func = dataRaw if fmt is None else fmt

    return map(func, dataMap), nbrFichier

def test(dossier) : 
    import matplotlib.pyplot as plt

    def autre(data) :
        Vg, time, Id, Is, Ig = data.T

        Vg = Vg[:100]
        time = time[:100]
        Id = Id[:100]
        Is = Is[:100]
        Ig = Ig[:100]

        I_bin = np.array([Is, Ig])
        yield Vg, time, Id, I_bin

    def autre2(data) :
        Vg, time, Id, Is, Ig = data.T

        Vg = np.reshape(Vg, shape=(2, -1))
        time = np.reshape(time, shape=(2, -1))
        Id = np.reshape(Id, shape=(2, -1))
        Is = np.reshape(Id, shape=(2, -1))
        Ig = np.reshape(Ig, shape=(2, -1))

        I_bin = np.array([Is, Ig])

        for i in range(2) :
            yield Vg[i], time[i], Id[i], I_bin[:, i]

    dataMap, nbrData = extractTC(dossier, fmt=autre2)

    for data in dataMap :
        for Vg, time, Id, I_bin in data :
            plt.plot(Vg, Id)
            
    plt.show()

if __name__ == "__main__" :
    test("data/data_PV/TC_good/")
