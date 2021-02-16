from scipy.stats import *
import numpy as np
import scipy.stats as st
import csv

""" On représente les classes de valeurs en utilisant la borne sup de chaque intervalle :
    les classes [0,0.3], ]0.3,0.6], ]0.6,0.8], ]0.8,1] sont représentées par [0.3,0.6,0.8,1]
"""
categories = [0.3,0.6,0.8,1]

class Profile :
    """ Classe représentant le profil d'un joueur
    """
    def __init__(self,actions_stats_csv,name) :
        self.name = name
        self.actions_stats = {}
        for c in categories :
            self.actions_stats[str(c)] = {}
        with open(actions_stats_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader :
                r = dict(row)
                self.actions_stats[r['hand_value']][r['action']]=float(r['value'])
        csvfile.close()
    def get_frequencies_from_category(self,cat) :
        """ Fonction retournant les fréquences de coups du profil pour la classe de valeurs cat
        """
        return np.array([self.actions_stats[str(cat)]['Fold'],self.actions_stats[str(cat)]['Check'],self.actions_stats[str(cat)]['Call'],self.actions_stats[str(cat)]['Raise']])

class Actions :
    """ Classe pour le traitement des actions d'un joueur :
        recorded_actions : dictionnaire contenant les différents coups joué par le joueur
    """
    def __init__(self,actions_csv) :
        self.recorded_actions = {}
        for x in categories :
            self.recorded_actions[str(x)]={'Fold':0,'Check':0,'Call':0,'Raise':0}
        with open(actions_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader :
                r = dict(row)
                self.recorded_actions[self.get_category(r['hand_value'])][r['action']]+=1
        csvfile.close()

    def get_category(self,x) :
        """ fonction interne
        """
        for y in categories :
            if float(x) < y :
                return str(y)
        return "No catetory"

    def get_numbers_from_category(self,cat) :
        """ fonction retournant le tableau des effectifs pour la classe de valeur cat
        """
        return np.array([self.recorded_actions[str(cat)]['Fold'],self.recorded_actions[str(cat)]['Check'],self.recorded_actions[str(cat)]['Call'],self.recorded_actions[str(cat)]['Raise']])

    def get_best_profile(self,profiles) :
        pvaluesAvForEachProfile = np.array([])
        # Pour chaque profil (Passif/large, Passif/serré…),
        for profile in profiles:
            # nous allons calculer la p-value moyenne,
            pvalueAvForEachCategory = np.array([])
            # elle correspondra à la p-value moyenne des actions (Fold, Call…),
            for category in categories:
                eff_obs = np.array([])
                for value in self.recorded_actions[str(category)]:
                    eff_obs = np.append(eff_obs, self.recorded_actions[str(category)][value])
                freq_obs = eff_obs/np.sum(eff_obs)
                freq_th = profile.get_frequencies_from_category(category)
                # qui elle correspondra à la p-value entre le profil courant, l’action courante et les données du joueur.
                pvalueAvForEachCategory = np.append(pvalueAvForEachCategory, st.chisquare(f_obs = freq_obs, f_exp = freq_th).pvalue)
            pvaluesAvForEachProfile = np.append(pvaluesAvForEachProfile, sum(pvalueAvForEachCategory)/len(pvalueAvForEachCategory))
        res = profiles[np.where(np.isclose(pvaluesAvForEachProfile, max(pvaluesAvForEachProfile)))[0][0]].name
        return res


def fonction_principale() :
    agg_serr = Profile("actions_agressif_serre.csv","Agressif/serré")
    agg_larg = Profile("actions_agressif_large.csv","Agressif/large")
    pass_serr = Profile("actions_passif_serre.csv","Passif/serré")
    pass_larg = Profile("actions_passif_large.csv","Passif/large")

    profiles = [agg_larg,agg_serr,pass_larg,pass_serr]

    actions_joueurA = Actions("joueurA.csv")
    actions_joueurB = Actions("joueurB.csv")
    actions_joueurC = Actions("joueurC.csv")
    actions_joueurD = Actions("joueurD.csv")
    actions_joueurE = Actions("joueurE.csv")
    actions_joueurF = Actions("joueurF.csv")

    print("Joueur A : "+actions_joueurA.get_best_profile(profiles))
    print("Joueur B : "+actions_joueurB.get_best_profile(profiles))
    print("Joueur C : "+actions_joueurC.get_best_profile(profiles))
    print("Joueur D : "+actions_joueurD.get_best_profile(profiles))
    print("Joueur E : "+actions_joueurE.get_best_profile(profiles))
    print("Joueur F : "+actions_joueurF.get_best_profile(profiles))

if __name__ == "__main__" :
    fonction_principale()
