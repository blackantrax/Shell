#! /usr/bin/python3
#-*- coding: utf-8 -*-
# Nom: Kevin Nelson Moudio
# DA: 1769692
# Prof. Mr Eric W.
# Dans le cadre du cours de Systeme d'exploitation
# TP 2
# Version 7.0

import os
import sys
import signal
listeProcess = []  # Variable Globale permettant de faire liste des processus en cours d'exécution


"""
Méthode main permettant de lancer le programme
Elle ne prends aucune valeur en parametre et le seul moyen de terminer le programme
Est d'utiliser la commande <quitter>
"""
def main():
    os.system("reset") # Permet de nettoyer le terminal afin de débuter l'exécution au nom de l'utilisateur
    global listeProcess # Variable Globale
    signal.signal(signal.SIGCHLD,fermetureProgramme) # Permet de détecter le signal lorsqu'un processus meurt et
                                                     # de faire une opération quelquonque
    listeDesProcessus = []
    terminer = False # Variable booléene permettant de lancer le programme dans une boucle infinie
    
	while not terminer:
        commande = debutProgramme() # Récupération de la commande de l'utilisateur
        args = commande.split(" ") # Conversion de la commande de type (str) en liste/Tableau
        if args[0].rstrip() == "liste" and len(args) == 1: # On vérifie si la commande entrée est <liste>
            if len(listeProcess) == 0: # Si la liste des Processus est vide, on affiche un message
                print("Il n y a pas de processus dans la liste",flush=True)
            else:
                lister() # Fonction qui permet de lister les processus en cours d'execution
        elif args[0].rstrip() == "tuer" and len(args) == 2: # On vérifie si la commande entrée est <tuer>
            killProcess(args) # Fonction qui permet de tuer un processus
        elif args[0].rstrip() == "quitter" and len(args) == 1: # On vérifie si la commande entrée est <quitter>
            quitterProgramme() # Fonction qui permet de quitter le programme
        else:
            listeDesProcessus = declencherProcessus(args) # Fonction qui permet d'exécuter des commandes
            listeProcess.append((args[0],listeDesProcessus[0],listeDesProcessus[1])) # Ajout du nom de la commande
                                                                                    #  Du PID et du tube dans la liste
                                                                                    # des Process en execution
            #if args[0] == "ls":
             #   os.system("sleep 0.1s")


"""
Cette fonction ne prends aucune variable en parametre et retourne la commande de l'utilisateur
La commande en question est intialisee par une chaine vide
Il y a dans la fonction une boucle while qui redemande a l'utilisateur de rentrer a nouveau sa chaine tant qu'il rentre
une chaine vide.
Si des le debut de l'execution du programme, l'utilisatuer fait un <CTRL+C> afin de quitter, le programme lui
demande une autre commande;
Le seul moyen de quitter est d'utiliser la commande <quitter>  
"""
def debutProgramme():
    chaine = "$?> "
    userShell = os.getlogin()+chaine # nom d'utilisateur +<tilt>
    commande = " "
    while len(commande.strip()) == 0:
        try:
            commande = input(userShell)
        except (KeyboardInterrupt,SystemExit):
            pass
            print() # Retour à la ligne après l'affichage

    return commande

def fermetureProgramme(SIGCHLD,handler):
    (pid, status) = os.wait()
    for process_name, pid_value, mistake in listeProcess:
        if pid_value == pid:
            if status != 0:
                pipe = mistake
                lecteur = os.fdopen(pipe[0])
                fichierEnregistrement = open("erreurs.txt",'a')
                print("########################################################################## \n",file=fichierEnregistrement,end="")
                print(str(listeProcess[0][0])+"\n",file=fichierEnregistrement,end="")
                for ligne in lecteur:
                    print(ligne,file=fichierEnregistrement,end="")
                lecteur.close()
                fichierEnregistrement.close()
            print("Le processus {0} est termine".format(pid_value)) # Affichage du Processus mort; Il est represente ici
                                                                    # Par son PID
																	
            listeProcess.remove((process_name, pid_value, mistake)) #Extraction du Processus mort de la liste des
                                                                    #Processus en cours d'execution

"""
Cette fonction permet de lister les processus en cours d'execution
Elle ne prends aucune variable en parametre parce qu'elle utilise le tableau  
de liste qui a ete declare comme une variable globale;
"""
def lister():
    for process_name, pid_value, mistake in listeProcess:
        print("{0}   {1}".format(process_name , pid_value)) # Affichage du nom de programme et de son PID,
                                                            # Separes par un espace.

"""
Cette methode prends en argument la commande <tuer> et le <pid> du programme a supprimer de la liste
On supprime ensuite le Processus grace a la commande <kill>
Dans le cas ou le PID n'existe pas dans la liste des Processus en cours d'execution par le programme,
le <try ... expect> permet de capturer deux types d'erreurs:
1- ProcessLookupError: Qui est genere lorsque le processus n'existe pas dans la liste
2- ValueError qui est genere lorsque l'utilisateur entre un type autre qu'un entier type(<int>)
"""
def killProcess(args):
    try:
        os.kill(int(args[1]),signal.SIGKILL)
    except (ProcessLookupError,ValueError):
        print("Processus n'est pas dans la liste des Processus")

		
"""
Cette fonction permet de declencher les programmes que l'utilisateur souhaite executer
Elle prends en parametre la commande de l'utilisateur,
Il y a ensuite la creation d'une copie du Processus pere (un fils)
qui sera charge d'executer la commande.
Une fois la commande executee, le pere se chargera ensuite de l'afficher
On se reserve quand meme la possibilite selon laquelle la fonction ne reussi pas a creer le 
processus fils,cas dans lequel on ecrit l'erreur a la sortie d'erreur.
"""
def declencherProcessus(commande):
    pipe = os.pipe()
    creationFils = os.fork()   # Creation du fils
    donnees  = []   # Tableau qui contient le PID et le pipe

    if creationFils == 0:  # Portion du code executer par le fils
        os.close(pipe[0])
        os.dup2(pipe[1],2) # Redirection de la sortie du programme
        os.execvp(commande[0],commande) # execution de la commmande entree par l'utilisateur

		elif creationFils > 0:   # Portion du code executer par le pere
        os.close(pipe[1])
        print("Programme {0} déclenché avec le PID {1}".format(commande[0],creationFils))
		donnees = [creationFils,pipe] # Insertion du PID et du tube dans un tableau (<donnees>)
        
		return donnees
    
	else:
        print("Le processus n'a pas pu démarrer", file = sys.stderr, end="")
        donnees = [creationFils, pipe] # Insertion du PID et du tube dans un tableau (<donnees>)
        
		return donnees

"""
Cette fonction permet, comme son nom l'indique, de quitter le programme.
Elle ne prends aucune valeur en parametre et ne retourne rien non plus.
Au debut de son execution, elle verifie la liste des Processus afin de s'assurer qu'elle soit vide;
Si la liste est vide, elle affiche un message <Aurevoir :)  !> et ferme le programme
Dans le cas ou la liste des Processus n'est pas vide, on demande a l'utilisateur si il veut tuer 
tous les processus dans la liste;
Si il dit OUI(o ou O), on tue tous les processus et on sort du programme.
Si il dit non, on le retourne au debut du programme 
"""
def quitterProgramme():
    if len(listeProcess) == 0:
        print("Aurevoir :) !")
        sys.exit(0)

    elif len(listeProcess) != 0:
        print("Il reste des processus actifs: ")
        lister()
        x = input("Voulez-vous les tuer (o/n) ?")

        if x == "o" or x =="O":
            for process_name, pid_value, mistake in listeProcess: # On Boucle tant qu'on a pas tuer tous les processus
                os.kill(pid_value,signal.SIGKILL)                 # presents dans la liste
            sys.exit(0)  # Sortie du programme

""" 
Entree du Programme
"""
if __name__ == '__main__':
    main()