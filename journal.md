# journal de bord


## 25 février 2026

Première version de l'ajustement de courbe TC par la fonction numérique double erf

Les tests sont en partie inconclusif en grande partie du au fait que la fonction à ajuster est complexe et curve\_fit ne trouve pas trivialement les paramètres.

Première version d'ajustement de courbe :
- Couper la TC en 2, avant le V\_cnp et après, et faite le curve fit d'une sigmoids * erf sur les segments.
- Permet de ressortir des paramètres proches des bons pour aider le curve\_fit total à bien trouver la réponse

Il est cependant dur de bien déterminer si le curve\_fit fonctionne pour le moment dû à la complexité, mais aussi du au fait que les jeux de donné que Paul m'a envoyé est loin d'être parfait, il est donc pas facile de déterminé si les erreurs de fit sont dû à quel facteur.

Tout de même, les fits ont la bonne alure, sauf pour quelque exception

Il serait aussi important de faire un vrai protocole de lecteur de donné CSV pour prendre en compte le fait que le data ne va pas nécéssairement être symétrique (le forward et la backward ne se font pas à la même vitesse) et que des fois je vais vouloir le data ravel et des fois non. Il sera donc très important de faire un vrai protocole de lecture de donné, comme pour les fichier TDMS.

#### Je pense aussi qui serait TRÈS pertinent de "resimuler" les courbes de TC avec les paramètres ajusté en modélisant le potentiel VG.

Le potentiel Vg est non trivial, une courbe Vg en fonction du temps montre que le Vg n'est pas mesuré équidistant, il est donc plus que probable que ça vient ajouter des erreurs dans le Id qui pourrait être "prédit" en resimulant les TC

Cette méthode pourrait aussi permettre de trouver les point de EDC que LP avait amené.

`I_V sweep LG mgf2_2_2.csv` semble avoir ce point de EDC justement

#### il sera peut-être important aussi de détermine la fréquence à laquelle les TC ont été prisent pour voir si les paramètres mesuré sont en accord avec les attentes

