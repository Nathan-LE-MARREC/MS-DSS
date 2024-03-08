import tkinter as tk
from tkinter import messagebox
import math

RAYON_TERRE = 6371  # en kilomètres

def calculer_periode_orbitale(type_orbite, *args):
    if type_orbite.lower() == "circulaire":
        rayon_orbite = args[0]
        demi_grand_axe = rayon_orbite + RAYON_TERRE
    elif type_orbite.lower() == "elliptique":
        apogee = args[0]
        perigee = args[1]
        demi_grand_axe = (apogee + perigee + 2 * RAYON_TERRE) / 2
    else:
        print("Type d'orbite non pris en charge.")
        return None
    
    # Calcul de la période orbitale en secondes
    periode_orbitale = 2 * math.pi * (demi_grand_axe ** 1.5) / (398600 ** 0.5)
    # Conversion de la période orbitale en minutes
    periode_orbitale_minutes = periode_orbitale / 60
    return periode_orbitale_minutes, demi_grand_axe

def calculer_vitesse(demi_grand_axe, periode_orbitale_minutes):
    # Calcul de la vitesse en km/s
    vitesse_kmps = (2 * math.pi * demi_grand_axe) / (periode_orbitale_minutes * 60)
    # Conversion de la vitesse en km/h
    vitesse_kmph = vitesse_kmps * 3600
    return vitesse_kmps, vitesse_kmph

def calculer_temps_ombre_soleil(demi_grand_axe, periode_orbitale_minutes):
    # Calcul de l'angle à l'ombre en radians
    angle_ombre = 2 * math.asin(RAYON_TERRE / demi_grand_axe)
    # Calcul de la durée à l'ombre en pourcentage
    pourcentage_ombre = (angle_ombre / (2 * math.pi)) * 100
    # Calcul du temps passé à l'ombre en minutes
    temps_ombre_minutes = pourcentage_ombre * periode_orbitale_minutes / 100
    # Calcul du temps passé au soleil en minutes
    temps_soleil_minutes = periode_orbitale_minutes - temps_ombre_minutes
    return temps_ombre_minutes, temps_soleil_minutes

def calculer_orbite():
    type_orbite = type_orbite_var.get()
    apogee = apogee_entry.get()
    perigee = perigee_entry.get()
    rayon_orbite = rayon_entry.get()
    
    if type_orbite.lower() == "circulaire":
        demi_grand_axe = float(rayon_orbite) + RAYON_TERRE
    elif type_orbite.lower() == "elliptique":
        demi_grand_axe = (float(apogee) + float(perigee) + 2 * RAYON_TERRE) / 2
    elif type_orbite.lower() == "circulaire":
        demi_grand_axe = float(rayon_orbite) + RAYON_TERRE
    else:
        messagebox.showerror("Erreur", "Type d'orbite non pris en charge.")
        return
    
    periode_orbitale_minutes, demi_grand_axe = calculer_periode_orbitale(type_orbite, float(apogee), float(perigee))
    temps_ombre_minutes, temps_soleil_minutes = calculer_temps_ombre_soleil(demi_grand_axe, periode_orbitale_minutes)
    vitesse_kmps, vitesse_kmph = calculer_vitesse(demi_grand_axe, periode_orbitale_minutes)
    
    result_label.config(text=f"Période orbitale (minutes): {periode_orbitale_minutes:.2f}\n"
                             f"Temps passé à l'ombre (minutes): {temps_ombre_minutes:.2f}\n"
                             f"Temps passé au soleil (minutes): {temps_soleil_minutes:.2f}\n"
                             f"Vitesse du satellite (km/s): {vitesse_kmps:.2f}\n"
                             f"Vitesse du satellite (km/h): {vitesse_kmph:.2f}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Calculateur d'orbite")

# Créer les widgets
type_orbite_label = tk.Label(root, text="Type d'orbite:")
type_orbite_label.grid(row=0, column=0, padx=5, pady=5)
type_orbite_var = tk.StringVar()
type_orbite_var.set("Circulaire")
type_orbite_option = tk.OptionMenu(root, type_orbite_var, "Circulaire", "Elliptique")
type_orbite_option.grid(row=0, column=1, padx=5, pady=5)

apogee_label = tk.Label(root, text="Apogée (km):")
apogee_label.grid(row=1, column=0, padx=5, pady=5)
apogee_entry = tk.Entry(root)
apogee_entry.grid(row=1, column=1, padx=5, pady=5)

perigee_label = tk.Label(root, text="Périgée (km):")
perigee_label.grid(row=2, column=0, padx=5, pady=5)
perigee_entry = tk.Entry(root)
perigee_entry.grid(row=2, column=1, padx=5, pady=5)

rayon_label = tk.Label(root, text="Rayon de l'orbite (km):")
rayon_label.grid(row=3, column=0, padx=5, pady=5)
rayon_entry = tk.Entry(root)
rayon_entry.grid(row=3, column=1, padx=5, pady=5)

def afficher_entrees(event):
    type_orbite = type_orbite_var.get()
    if type_orbite.lower() == "circulaire":
        apogee_label.grid_remove()
        apogee_entry.grid_remove()
        perigee_label.grid_remove()
        perigee_entry.grid_remove()
        rayon_label.grid(row=1, column=0, padx=5, pady=5)
        rayon_entry.grid(row=1, column=1, padx=5, pady=5)
    elif type_orbite.lower() == "elliptique":
        rayon_label.grid_remove()
        rayon_entry.grid_remove()
        apogee_label.grid(row=1, column=0, padx=5, pady=5)
        apogee_entry.grid(row=1, column=1, padx=5, pady=5)
        perigee_label.grid(row=2, column=0, padx=5, pady=5)
        perigee_entry.grid(row=2, column=1, padx=5, pady=5)

type_orbite_option.bind("<Button-1>", afficher_entrees)

calculate_button = tk.Button(root, text="Calculer", command=calculer_orbite)
calculate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Lancer la boucle principale
root.mainloop()
