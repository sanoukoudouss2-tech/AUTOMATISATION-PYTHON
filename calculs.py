"""Fonctions de calcul pour le dashboard support client (groupe 3).

Toutes les fonctions sont "pures" : elles lisent un DataFrame, calculent et
retournent un résultat, sans rien modifier à l'extérieur. Elles peuvent donc
être appelées telles quelles depuis les callbacks Dash.
"""

import pandas as pd

CHEMIN_CSV = "groupe_03_support_client.csv"

# Ordre d'affichage des priorités (à vérifier avec df["priorite"].value_counts()).
# Les valeurs absentes de cette liste sont ajoutées à la fin automatiquement.
ORDRE_PRIORITE = ["Critique", "Haute", "Moyenne", "Basse"]


# ----------------------------------------------------------------------
# Chargement (à appeler UNE SEULE FOIS, au démarrage, hors callback)
# ----------------------------------------------------------------------
def charger_donnees(chemin=CHEMIN_CSV):
    """Charge le CSV et ajoute la colonne `sla_respecte`.

    `sla_respecte` est calculée ligne par ligne : temps_resolution_h <= sla_heures.
    Elle vaut NaN quand le temps de résolution est inconnu (ticket non résolu),
    pour que ces tickets ne faussent pas le taux de respect du SLA.
    """
    df = pd.read_csv(chemin, parse_dates=["date_ouverture"])
    respecte = (df["temps_resolution_h"] <= df["sla_heures"]).astype("float")
    df["sla_respecte"] = respecte.where(df["temps_resolution_h"].notna())
    return df


# ----------------------------------------------------------------------
# Filtrage
# ----------------------------------------------------------------------
def _en_liste(valeur):
    """None -> None ; 'a' -> ['a'] ; liste -> liste (vide -> None = pas de filtre)."""
    if valeur is None:
        return None
    if isinstance(valeur, (list, tuple, set)):
        return list(valeur) or None
    return [valeur]


def filtrer(df, debut=None, fin=None, canaux=None, categories=None,
            priorites=None, agents=None):
    """Applique tous les filtres du dashboard et retourne un nouveau DataFrame.

    - debut / fin : bornes de dates, fin INCLUSE (toute la journée de `fin`).
    - canaux, categories, priorites, agents : valeur, liste, ou None (= tout).
    """
    d = df
    if debut is not None:
        d = d[d["date_ouverture"] >= pd.to_datetime(debut)]
    if fin is not None:
        d = d[d["date_ouverture"] < pd.to_datetime(fin) + pd.Timedelta(days=1)]

    for colonne, valeurs in [("canal", canaux), ("categorie", categories),
                             ("priorite", priorites), ("agent", agents)]:
        valeurs = _en_liste(valeurs)
        if valeurs is not None:
            d = d[d[colonne].isin(valeurs)]
    return d


# ----------------------------------------------------------------------
# KPI
# ----------------------------------------------------------------------
def nb_tickets(d):
    """Nombre de tickets ouverts sur la période filtrée."""
    return int(len(d))


def nb_tickets_non_resolus(d):
    """Nombre de tickets encore non résolus (colonne `resolu`)."""
    return int((~d["resolu"].astype(bool)).sum())


def taux_sla(d):
    """Part des tickets (résolus) traités dans le SLA, en %. None si aucun ticket."""
    serie = d["sla_respecte"].dropna()
    if serie.empty:
        return None
    return float(serie.mean() * 100)


def satisfaction_moyenne(d):
    """Note moyenne de satisfaction (1 à 5). None si aucune note."""
    serie = d["satisfaction_1_5"].dropna()
    if serie.empty:
        return None
    return float(serie.mean())


def premiere_reponse_moyenne(d):
    """Temps moyen de première réponse, en minutes (4e KPI proposé)."""
    serie = d["premiere_reponse_min"].dropna()
    if serie.empty:
        return None
    return float(serie.mean())


# ----------------------------------------------------------------------
# Données pour les graphiques
# ----------------------------------------------------------------------
def tickets_par_jour(d):
    """Graphique 1 : nombre de tickets ouverts par jour (jours sans ticket = 0)."""
    if d.empty:
        return pd.DataFrame({"date": [], "tickets": []})
    serie = d.set_index("date_ouverture").resample("D").size()
    return serie.rename("tickets").rename_axis("date").reset_index()


def _trier_priorites(valeurs):
    connues = [p for p in ORDRE_PRIORITE if p in valeurs]
    inconnues = sorted(set(valeurs) - set(ORDRE_PRIORITE))
    return connues + inconnues


def sla_par_priorite(d):
    """Graphique 2 : taux de respect du SLA (%) par priorité, calculé ligne par ligne."""
    r = (d.dropna(subset=["sla_respecte"])
           .groupby("priorite")["sla_respecte"].mean().mul(100))
    r = r.reindex(_trier_priorites(r.index)).rename("taux_sla_pct")
    return r.reset_index()


def charge_par_agent(d):
    """Graphique 3 : nombre de tickets par agent, du plus chargé au moins chargé."""
    r = d["agent"].value_counts().rename("tickets").rename_axis("agent")
    return r.reset_index()


def temps_resolution(d):
    """Graphique 4 : série des temps de résolution (h) pour l'histogramme."""
    return d["temps_resolution_h"].dropna()


# ----------------------------------------------------------------------
# Aide à la conclusion (question d'analyse)
# ----------------------------------------------------------------------
def stats_par_priorite(d):
    """Tableau de synthèse par priorité pour répondre à la question d'analyse :
    "Les tickets critiques sont-ils traités en priorité, et au prix de quels autres ?"
    """
    g = d.groupby("priorite")
    t = pd.DataFrame({
        "tickets": g.size(),
        "premiere_reponse_moy_min": g["premiere_reponse_min"].mean(),
        "resolution_mediane_h": g["temps_resolution_h"].median(),
        "taux_sla_pct": g["sla_respecte"].mean() * 100,
        "reouvertures_moy": g["reouvertures"].mean(),
        "satisfaction_moy": g["satisfaction_1_5"].mean(),
    })
    return t.reindex(_trier_priorites(t.index)).round(2)


# ----------------------------------------------------------------------
# Test rapide : python calculs.py
# ----------------------------------------------------------------------
if __name__ == "__main__":
    donnees = charger_donnees()
    print(donnees.info())
    print("Tickets          :", nb_tickets(donnees))
    print("Non résolus      :", nb_tickets_non_resolus(donnees))
    print("Taux SLA (%)     :", taux_sla(donnees))
    print("Satisfaction     :", satisfaction_moyenne(donnees))
    print("1re réponse (min):", premiere_reponse_moyenne(donnees))
    print(stats_par_priorite(donnees))