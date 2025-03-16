# -*- coding: utf-8 -*-
"""
@author: mathf
"""

import numpy as np
from tkinter import *
import time

def double_pendule_euler(theta1_0, theta2_0, omega1_0, omega2_0, m1, m2, l1, l2, g, dt, n_etapes):
    '''Résolution de l'équation différentielle avec la méthode d'euler'''
    theta1, theta2 = theta1_0, theta2_0
    omega1, omega2 = omega1_0, omega2_0
    theta1_results = np.zeros(n_etapes)
    theta2_results = np.zeros(n_etapes)

    for i in range(n_etapes):
        theta1_results[i] = theta1
        theta2_results[i] = theta2
        # équation différentielle :
        alpha1 = (-g*(2*m1+m2)*np.sin(theta1)-m2*g*np.sin(theta1-2*theta2)-2*np.sin(theta1-theta2)*m2*(omega2**2*l2+omega1**2*l1*np.cos(theta1-theta2)))/(l1*(2*m1+m2-m2*np.cos(2*theta1-2*theta2)))
        alpha2 = (2*np.sin(theta1-theta2)*(omega1**2*l1*(m1+m2)+g*(m1+m2)*np.cos(theta1)+omega2**2*l2*m2*np.cos(theta1-theta2)))/(l2*(2*m1+m2-m2*np.cos(2*theta1-2*theta2)))
        omega1 += alpha1 * dt
        omega2 += alpha2 * dt
        theta1 += omega1 * dt
        theta2 += omega2 * dt
    return theta1_results, theta2_results

# Caractéristique du pendule
pi = np.pi
m1 = 1                
m2 = 1                
l1 = 1                
l2 = 1                
g = 9.81              
dt = 0.01             
n_etapes = 1000        

time_start = 0

# Fonctions qui intégrent la simulation dans une interface graphique

def lancer_simulation(trace=False):
    ''' Lancement de la simulation'''
    global theta1_results, theta2_results, time_start, n_etapes,couleurs
    
    theta1_0 = eval(entree_theta1_0.get())
    theta2_0 = eval(entree_theta2_0.get())
    omega1_0 = eval(entree_omega1_0.get())
    omega2_0 = eval(entree_omega2_0.get())
    n_etapes = eval(entree_N.get())
    dt = eval(entree_dt.get())
    g = eval(entree_g.get())

    theta1_results, theta2_results = double_pendule_euler(theta1_0, theta2_0, omega1_0, omega2_0, m1, m2, l1, l2, g, dt, n_etapes)
    time_start = time.time()
    if len(liste_point1) == 0:
        couleurs= LISTE_COULEURS.copy()
    simulation(trace)
    
def lancer_simulation_trace():
    lancer_simulation(True)
    
last_step = 0
liste_point1 = []
LISTE_COULEURS = ['purple','red','blue','yellow','orange','green','red']
couleurs = []

def simulation(trace = False, clr = None):
    '''Tracé de la simulation sur l'interface'''
    global time_start, last_step, couleurs
    if clr == None:
        clr = couleurs.pop()
    if int((time_start-time.time())/dt) != last_step:
        last_step = int((time.time()-time_start)/dt)
        if last_step >= n_etapes-1:
            last_step = 0
            return None
        p1 = 100*l1*np.sin(theta1_results[last_step])
        p2 = 100*l1*np.cos(theta1_results[last_step])
        p3 = p1+100*l2*np.sin(theta1_results[last_step]+theta2_results[last_step])
        p4 = p2+100*l2*np.cos(theta1_results[last_step]+theta2_results[last_step])
        if trace:
            taille_cercle = 2
            taille_cercle = max(1,taille_cercle//2)
            liste_point1.append(canvas.create_oval(250+p3-taille_cercle,100+p4-taille_cercle, 250+p3+taille_cercle,100+p4+taille_cercle, fill=clr, width=0))
        canvas.coords(pendule1,250,100,250+p1,100+p2)
        canvas.coords(pendule2,250+p1,100+p2,250+p3,100+p4)
    def simu():
        simulation(trace,clr)
    fenetre.after(1,simu)
    
def effacer():
    global liste_point1
    for i in liste_point1:
        canvas.delete(fenetre,i)
    liste_point1 = []

# Création de l'interface
fenetre = Tk()
paned = PanedWindow(fenetre, orient = HORIZONTAL)
panedgauche = PanedWindow(paned,orient = VERTICAL)
paned.add(panedgauche)

panedgauche.add(Label(fenetre,text = 'theta1_0 :', anchor='w'))
entree_theta1_0 = Entry(fenetre)
entree_theta1_0.insert(0,"pi/2")
panedgauche.add(entree_theta1_0)

panedgauche.add(Label(fenetre,text = 'theta2_0 :',anchor='w'))
entree_theta2_0 = Entry(fenetre)
entree_theta2_0.insert(0,"pi/4")
panedgauche.add(entree_theta2_0)

panedgauche.add(Label(fenetre,text = 'omega1_0 :',anchor='w'))
entree_omega1_0 = Entry(fenetre)
entree_omega1_0.insert(0,"0")
panedgauche.add(entree_omega1_0)

panedgauche.add(Label(fenetre,text = 'omega2_0 :',anchor='w'))
entree_omega2_0 = Entry(fenetre)
entree_omega2_0.insert(0,"0")
panedgauche.add(entree_omega2_0)

panedgauche.add(Label(fenetre,text = 'N :',anchor='w'))
entree_N = Entry(fenetre)
entree_N.insert(0,"1000")
panedgauche.add(entree_N)

panedgauche.add(Label(fenetre,text = 'dt :',anchor='w'))
entree_dt = Entry(fenetre)
entree_dt.insert(0,"0.01")
panedgauche.add(entree_dt)

panedgauche.add(Label(fenetre,text = 'g :',anchor='w'))
entree_g = Entry(fenetre)
entree_g.insert(0,"9.81")
panedgauche.add(entree_g)

paneddroite = PanedWindow(paned,orient = VERTICAL)
paned.add(paneddroite)


canvas = Canvas(paneddroite, height = 600, width = 500, bg = 'white')
pendule1 = canvas.create_line(250,100,250,100)
pendule2 = canvas.create_line(250,100,250,100)

#100 pixel -> 1 unité de longueur
paneddroite.add(canvas)
bouton = Button(fenetre, text = 'Lancer la simulation', command = lancer_simulation)
paneddroite.add(bouton)

bouton = Button(fenetre, text = 'Lancer la simulation en traçant les points', command = lancer_simulation_trace)
paneddroite.add(bouton)
paneddroite.add(Button(fenetre,text="Effacer",command=effacer))

paned.pack()

fenetre.title('Double pendule')
fenetre.mainloop()



