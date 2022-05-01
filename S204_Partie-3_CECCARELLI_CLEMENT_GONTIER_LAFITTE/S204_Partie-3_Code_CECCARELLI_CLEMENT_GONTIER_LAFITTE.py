import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def initialize_matplotlib():
    fig, ax = plt.subplots()
    plt.xticks(rotation=-20)
    plt.style.use("seaborn-dark")
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'
    ax.grid(color='#2A3459')
    return fig, ax

def diagramme1(NOMM, export=False):

    # Récupération des données
    RT1 = pd.merge(RELEVE, MESURE, on="IDR")    # Ajout des relevés sur les mesures
    RT2 = pd.merge(RT1, STATION, on="IDS")      # Ajout des stations
    RT3 = pd.merge(RT2, LIEU, on="IDL")         # Ajout des lieux
    RT4 = RT3.loc[RT3["NOMM"] == NOMM]          # Sélection des mesures dont le nom est passé en paramètre
    villes = RT4["NOML"].unique()               # Récupération de la liste des villes

    # Affichage du graphique
    ax.set_ylabel(NOMM)
    ax.set_title(f'Evolutions : {NOMM}')
    couleurs = ['#F91E53','#C2185B','#9C27B0','#5727B0','#272AB0','#276BB0']

    for i in range(len(villes)):
        RT5 = RT4.loc[RT4["NOML"] == villes[i]]     # Sélection des mesures dans la ville concernée
        RT6 = RT5.groupby(["DATER"]).mean()     # Regroupement par date (moyenne des mesures) pour avoir une unique mesure par jour
        dates = RT6.index
        mesures = RT6["MESURE"]
        plt.plot(dates, mesures, marker='o', color=couleurs[i])

    # Affichage de la légende
    ax.legend(villes, loc="center left", bbox_to_anchor=(1, 0.5))

    plt.show()

    # Exportation
    if export:
        plt.savefig(f"evolutions_{NOMM}.png")

def diagramme2(NOMM, export=False):

    # Récupération des données
    RT1 = pd.merge(RELEVE, MESURE, on="IDR")    # Ajout des relevés sur les mesures
    RT2 = pd.merge(RT1, STATION, on="IDS")      # Ajout des stations
    RT3 = pd.merge(RT2, LIEU, on="IDL")         # Ajout des lieux
    RT4 = RT3.loc[RT3["NOMM"] == NOMM]          # Sélection des mesures prises dans la ville passé en paramètre
    RT5 = RT4.groupby(["NOML"]).mean()          # Regroupement par ville (moyenne des mesures)

    # Affichage du graphique
    villes = RT5.index
    temperatures = RT5["MESURE"]
    ax.set_ylabel(NOMM)
    ax.set_title(f'Moyennes : {NOMM}')
    plt.bar(villes, temperatures, width=0.5, color=['#F91E53','#C2185B','#9C27B0','#5727B0','#272AB0','#276BB0'])

    plt.show()

    # Exportation
    if export:
        plt.savefig(f"moyennes_{NOMM}.png")

def diagramme3(NOML, export=False):

    # Récupération des données
    IDL = LIEU.loc[LIEU["NOML"] == NOML]["IDL"].values[0]   # ID de la région passée en paramètre
    RT = ALERTE.loc[ALERTE["IDL"] == IDL]                   # Alertes enregistrées dans la région

    # Ajout de nouvelles données
    debut = RT["DATEDEB"].min()                     # Première date présente dans la table
    RT['STARTNUM'] = (RT["DATEDEB"]-debut).dt.days  # Ajout d'un attribut qui compte le nombre de jours écoulés entre le début d'une alerte et le début de la première alerte
    RT['ENDNUM'] = (RT["DATEFIN"]-debut).dt.days    # Ajout d'un attribut qui compte le nombre de jours écoulés entre la fin d'une alerte et le début de la première alerte
    RT['DUREE']= RT["ENDNUM"] - RT["STARTNUM"]      # Ajout d'un attribut pour la durée d'une alerte (en nombre de jours)

    # Ajout d'un attribut COULEUR qui correspond au RGB du niveau d'alerte
    def color(row):
        c_dict = {'Vert':'#3A9D23', 'Jaune':'#FFE436', 'Orange':'#E77500', 'Rouge':'#FF073A'}
        return c_dict[row['NIVEAU']]
    RT['COULEUR'] = RT.apply(color, axis=1)

    # Affichage du diagramme
    Y = RT["CATEGORIE"]
    start = RT["STARTNUM"]
    size = RT["DUREE"]
    colors = RT["COULEUR"]
    ax.set_title(f'Alertes en {NOML} en 2021')

    ax.barh(Y, size, left=start, color=colors)

    xticks = np.arange(0, RT["ENDNUM"].max()+1, 37)
    xticks_labels = pd.date_range(debut, end=RT["DATEFIN"].max()).strftime("%d/%m")
    xticks_minor = np.arange(0, RT["ENDNUM"].max()+1, 1)
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::37])

    plt.show()

    # Exportation
    if export:
        plt.savefig(f"alertes_{NOML}.png")

def diagramme4(NOMM, export=False):

    # Récupération des données
    RT1 = pd.merge(RELEVE, MESURE, on="IDR")    # Ajout des relevés sur les mesures
    RT2 = pd.merge(RT1, STATION, on="IDS")      # Ajout des stations
    RT3 = pd.merge(RT2, LIEU, on="IDL")         # Ajout des lieux
    RT4 = RT3.loc[RT3["NOMM"] == NOMM]          # Sélection des mesures dont le nom est passé en paramètre
    villes = RT4["NOML"].unique()               # Récupération de la liste des villes

    # Affichage du graphique
    ax.set_ylabel(NOMM)
    ax.set_title(f'Répartitions : {NOMM}')
    couleurs = ['#F91E53','#C2185B','#9C27B0','#5727B0','#272AB0','#276BB0']

    for i in range(len(villes)):
        RT5 = RT4.loc[RT4["NOML"] == villes[i]]     # Sélection des mesures dans la ville concernée
        mesures = RT5["MESURE"]
        box = plt.boxplot(mesures, positions=[i+1], widths=[0.5], flierprops=dict(markeredgecolor=couleurs[i], markeredgewidth=2))
        for item in ['boxes', 'whiskers', 'medians', 'caps']:
            plt.setp(box[item], color=couleurs[i], linewidth=2)
    plt.xticks(range(1,len(villes)+1), villes)

    plt.show()

    # Exportation
    if export:
        plt.savefig(f"repartitions_{NOMM}.png")

if __name__ == "__main__":

    # Initialisation de matplotlib (style)
    fig, ax = initialize_matplotlib()

    # Importation des tables
    STATION = pd.read_excel("STATION.xlsx")
    RELEVE  = pd.read_excel("RELEVE.xlsx")
    MESURE  = pd.read_excel("MESURE.xlsx")
    LIEU    = pd.read_excel("LIEU.xlsx")
    ALERTE  = pd.read_excel("ALERTE.xlsx")

    # Choix du diagramme
    # Décommentez une ligne ci-dessous pour l'afficher

    # diagramme1("Temperature")
    # diagramme1("Precipitation")
    # diagramme1("Ensoleillement")
    # diagramme1("Vent")

    # diagramme2("Temperature")
    # diagramme2("Precipitation")
    # diagramme2("Ensoleillement")
    # diagramme2("Vent", True)

    # diagramme3("PROVENCE-ALPES-COTE-D-AZUR")
    # diagramme3("ILE-DE-FRANCE")

    # diagramme4("Temperature")
    # diagramme4("Precipitation")
    # diagramme4("Ensoleillement")
    # diagramme4("Vent")