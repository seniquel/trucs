# -*- coding: utf-8 -*-
#à optimiser
#-visualiser comment varie la plus grande distance au centre en fonction du nombre de particules générées
#-utiliser ces données pour réduire le plus possible la distance à laquelle la particule est générée par rapport à la figure
import matplotlib.pyplot as plt
import random as rd
import numpy as np

n=50000#nombre de particules générées

def add(x, y): return x+y

def plusmoins(x):
    dim=np.shape(grid)[0]
    a=rd.randint(-1,1)
    while x+a>(dim-1) or x+a<0 :  
        a=rd.randint(-1,1)
    return x+a
    
def listebords(y): #génère une liste des coordonnées de points aux bords de la matrice y
    dim=np.shape(y)[0]
    x=range(0)
    for i in range(dim):
        x.append([0,i])
        x.append([dim-1,i])
    for i in range(dim-2):
        x.append([i+1,0])
        x.append([i+1,dim-1])
    return x

def genpart(x,y,listarray): #génération d'une particule de coordonnées x sur une matrice y parmi la distribution de coordonnées listarray
    x=rd.choice(listarray)
    while y[x[0]][x[1]]!=0:
        x=rd.choice(listarray)
    return x
    
def mvtbrown(x,y): #déplacement d'une particule de coordonnées initiales x par marche aléatoire jusqu'à qu'elle soit adjacente à une autre particule dans la matrice y
    dim=np.shape(y)[0]
    while(y[x[0]+1-x[0]//(dim-1),x[1]] or y[x[0]-1+x[0]//(dim-1),x[1]] or y[x[0],x[1]+1-x[1]//(dim-1)] or y[x[0],x[1]-1+x[1]//(dim-1)]) ==0:
        x=map(plusmoins,x)
    return x
    
def checkplusloin(x,v,w): #vérifie quelle est la particule la plus éloignée du centre de la matrice x horizontalement ou verticalement et renvoie les coordonnées de la plus éloignée
    dim=np.shape(x)[0]
    dist1=max(abs((dim/2)-v[0]),abs((dim/2)-v[1]))
    dist2=max(abs((dim/2)-w[0]),abs((dim/2)-w[1]))
    if dist2>dist1:
        return w
    else:
        return v
    
def expandarray(x): #agrandit la matrice x de deux colonnes à gauche et à droite et de deux lignes en haut et en bas
    x=np.append(x,np.zeros([np.shape(x)[0],1]),1)
    x=np.append(np.zeros([np.shape(x)[0],1]),x,1)
    x=np.append(x,np.zeros([1,np.shape(x)[1]]),0)
    x=np.append(np.zeros([1,np.shape(x)[1]]),x,0)
    return x
    
def boxcountdim(x): #calcule la dimension de Minkowski-Bouligand de la matrice de la fractale x
    n=0    
    dim=np.shape(x)[0]
    pts=range(0)
    epsilon=range(0)
    endloop=False
    for d in range(int(np.log(dim)/np.log(2))-1):
        dimsub=dim/(2**(d+1)) #dimension de la matrice des sous-matrices d'indice d
        for I in range(dim/dimsub):
            for J in range(dim/dimsub):
                for i in range(dimsub):
                    for j in range(dimsub):
                        if x[dimsub*I+i][dimsub*J+j]!=0 and endloop==False:
                            n=n+1
                            endloop=True
                endloop=False                        
        if n!=0 and d>0:
            pts.append(np.log(n)/np.log(float(dim)/float(dimsub)))
            epsilon.append(float(dimsub)/float(dim))
        n=0
    coeffpoly=np.polyfit(epsilon,pts,3)
    fitpoly=np.poly1d(coeffpoly)
    res=fitpoly(0)
    return res

#initialisation de la grille de particules
grid=np.ones((1,1))
#initialisation des coordonnées (x,y) d'une nouvelle particule
coordpart=range(2)
bords=range(0)
distance=range(0)
plusloin=[0,0] #particule la plus éloignée du centre horizontalement ou verticalement
dim=np.shape(grid)[0]

for i in range(n):
    dim=max(abs((dim/2)-plusloin[0]),abs((dim/2)-plusloin[1]))*2+50
    while (np.shape(grid)[0]<=dim):
        grid=expandarray(grid)
        plusloin=map(add,plusloin,[1,1]) #la forme de la matrice change, il faut donc changer la position de plusloin
    bords=listebords(grid)
    coordpart=genpart(coordpart,grid,bords)
    coordpart=mvtbrown(coordpart,grid)
    grid[coordpart[0],coordpart[1]]=i+2
    plusloin=checkplusloin(grid,plusloin,coordpart)
    if i==100*(i//100):
        print i
plt.imshow(grid)

print "La dimension fractale de cette figure est :",boxcountdim(grid)