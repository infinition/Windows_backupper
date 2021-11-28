import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter import *

import os
import time

dir_list = []
folder_backup_name = "backup"+time.strftime("%Hh%M-%d-%m-%Y") #nom du dossier de sauvegarde pour le zip

#fonction qui demande quel répertoire on veut sauvegarder
# ajoute le répertoire à une liste de répertoire à sauvegarder dir_list et actualise la liste
def get_dir():
      #ouvrir une boite de dialogue pour choisir le répertoire
      dir_name = filedialog.askdirectory()
      #afficher le répertoire choisi dans la boite de dialogue
      dir_label.config(text=dir_name)
      #ajouter le répertoire à la liste de répertoire à sauvegarder
      dir_list.append(dir_name)
      show_dir_list()


#fonction qui permet de choisir le répertoire de destination de la sauvegarde
def get_dir2():
      #ouvrir une boite de dialogue pour choisir le répertoire
      dir_name = filedialog.askdirectory()
      #afficher le répertoire choisi dans la boite de dialogue
      dir_label2.config(text=dir_name)

#fait une sauvegarde des répertoires de la liste vers le répertoire de destination choisi
def backup_dir_list():
      #recuperer le nom du répertoire de destination
      dir_dest = dir_label2.cget("text")
      #si le répertoire de destination est vide
      if dir_dest == "":
            #afficher un message d'erreur
            messagebox.showerror("Erreur" , "Veuillez choisir un répertoire de destination")
      #sinon
      else:
            #pour chaque répertoire à sauvegarder
            for dir_name in dir_list:                            
                  #remplacer les retour à la ligne par des espaces vides
                  dir_name = dir_name.replace("\n", "")
                  #faire une copie du répertoire à sauvegarder vers le répertoire de destination 
                  os.system("cp -pr "+ "\""+ dir_name +"\""+ " " + "\""+dir_dest+"\"")
                  #Debug print("Dirname1: "+dir_name)
                  #Debug print("Dirdest: "+dir_dest)
                  #Debug print(dir_list)
            #afficher un message de confirmation de sauvegarde
            messagebox.showinfo("Backup", "Sauvegarde terminée")


def backup_dir_list_zip():
      #recuperer le nom du répertoire de destination
      dir_dest = dir_label2.cget("text")
      #si le répertoire de destination est vide
      if dir_dest == "":
            #afficher un message d'erreur
            messagebox.showerror("Erreur" , "Veuillez choisir un répertoire de destination")
      #sinon
      else:
            #pour chaque répertoire à sauvegarder
            for dir_name in dir_list:
                  #faire une copie du répertoire à sauvegarder vers le répertoire de destination et ajouter la date de sauvegarde
                  os.system("zip -r "+ "\""+ dir_dest + "/" + folder_backup_name  + ".zip"+"\" "+"\""+dir_name+"\"")
                  #os.system("zip -r " + dir_name + ".zip " + dir_name)
            #afficher un message de confirmation
            messagebox.showinfo("Backup", "Sauvegarde Zip terminée")


#fonction qui actualise la liste des répertoires à sauvegarder à chaque fois que l'on ajoute un répertoire à la liste
def show_dir_list():
      print(dir_list)
      if dir_list == []: #si la liste est vide
            tableau_dir_list.delete(*tableau_dir_list.get_children()) #supprimer toutes les lignes du tableau
            tableau_dir_list.insert("", "end", text="Aucun dossier selectionné") #ajouter une ligne dans le tableau avec le message "Aucun dossier selectionné"
      #sinon
      else:
            #vider la liste
            tableau_dir_list.delete(*tableau_dir_list.get_children())
            #pour chaque répertoire à sauvegarder
            for dir_name in dir_list:
                  #afficher le répertoire dans la liste
                  tableau_dir_list.insert("", "end", text=dir_name)

def clear_dir_list():
      #vider la liste des répertoires à sauvegarder
      dir_list.clear()
      #actualiser la liste
      show_dir_list()

#sauvegarder la configuration de la liste des répertoires à sauvegarder et le répertoire de destination dans un second fichier de configuration
def save_config_all():
      #ouvrir le fichier de configuration dans le même répertoire que le programme
      config_file_folder = open(os.path.dirname(os.path.realpath(__file__)) + "/config.txt", "w")
      #pour chaque répertoire à sauvegarder
      for dir_name in dir_list:
            #ecrire dans le fichier de configuration le nom du répertoire à sauvegarder
            config_file_folder.write(dir_name + "\n")

      #fermer le fichier de configuration      
      config_file_folder.close()
      #ouvrir le fichier de configuration dans le même répertoire que le programme
      config_file_dest = open(os.path.dirname(os.path.realpath(__file__)) + "/config_dest.txt", "w")
      #écrire le répertoire de destination dans le fichier de configuration
      config_file_dest.write(dir_label2.cget("text"))
      #fermer le fichier de configuration
      config_file_dest.close()
      #afficher un message de confirmation
      messagebox.showinfo("Sauvegarde", "Sauvegarde de la configuration réussie")

def load_config_all():
      dir_list.clear()
       #ouvrir le fichier de configuration dans le même répertoire que le programme
      config_file_folder = open(os.path.dirname(os.path.realpath(__file__)) + "/config.txt", "r")
      #pour chaque répertoire à sauvegarder dans le fichier de configuration 
      for dir_name in config_file_folder:
            #remplacer le retour à la ligne par une chaine vide
            dir_name = dir_name.replace("\n", "")
            #ajouter le répertoire à la liste des répertoires à sauvegarder
            dir_list.append(dir_name)
      #fermer le fichier de configuration
      config_file_folder.close()
      show_dir_list()
      #ouvrir le fichier de configuration dans le même répertoire que le programme
      config_file_dest = open(os.path.dirname(os.path.realpath(__file__)) + "/config_dest.txt", "r")
      #afficher le répertoire de destination dans la boite de dialogue
      dir_label2.config(text=config_file_dest.read())
      #fermer le fichier de configuration
      config_file_dest.close()
      #actualiser la liste


window = Tk()
window.title("Backupper")
window.geometry("900x500")
#ajuster la taille de la fenetre au contenu
#window.grid_columnconfigure(0, weight=1)
bouton = ttk.Button(window, text="Ajouter un répertoire à la liste de sauvegarde", command=get_dir)
bouton.grid(column=0, row=0)
dir_label = ttk.Label(window, text="", background="black", foreground="orange")
dir_label.grid(column=0, row=1)
bouton2 = ttk.Button(window, text="Choisir le répertoire de destination", command=get_dir2)
bouton2.grid(column=0, row=2)
dir_label2 = ttk.Label(window, text="", background="black", foreground="green")
# afficher en gras le texte du label
dir_label2.config(font=("Arial", 12, "bold"))
dir_label2.grid(column=0, row=3)
bouton3 = ttk.Button(window, text="Lancer la sauvegarde", command=backup_dir_list)
bouton3.grid(column=0, row=4)
bouton4 = ttk.Button(window, text="Lancer la sauvegarde (zip)", command=backup_dir_list_zip)
bouton4.grid(column=0, row=5)
#bouton5 = ttk.Button(window, text="Montrer la liste des dossiers", command=show_dir_list)
#bouton5.grid(column=0, row=6)
bouton6 = ttk.Button(window, text="Vider la liste et les champs", command=clear_dir_list)
#coller le bouton6 au bouton5
bouton6.grid(column=0, row=6)
bouton7 = ttk.Button(window, text="Sauvegarder la configuration", command=save_config_all)
bouton7.grid(column=0, row=7)
bouton8 = ttk.Button(window, text="Charger la configuration", command=load_config_all)
bouton8.grid(column=0, row=8)
tableau_dir_list = Treeview(window)
#ajouter le tableau à la fenetre, même quand la fenetre est redimensionnée
tableau_dir_list.grid(column=0, row=9, sticky=(N, S, E, W))
#tableau_dir_list.grid(column=0, row=9, columnspan=1, sticky="nsew")
tableau_dir_list.heading("#0", text="Liste des répertoires à sauvegarder")
tableau_dir_list.column("#0", stretch=True, minwidth=0, width=900)



window.mainloop()
     

            


