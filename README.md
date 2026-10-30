# Jeux de données par groupe — TP Dashboard (Dash)

**Module :** Automatisation Avancée avec Python · **Livrable :** une application Dash par groupe

Chaque groupe reçoit **son propre jeu de données**, avec un schéma et un métier différents.
Les 18 tableaux de bord rendus ne se ressemblent donc pas, et un groupe ne peut pas réutiliser
le travail d'un autre. Les fichiers sont dans `data/groupes/`.

## Attribution des jeux de données

| Groupe | Membres | Thème | Fichier | Lignes | Colonnes |
|---:|---|---|---|---:|---:|
| **1** | Choukri mohamed-Lassine Savani | Ventes e-commerce | `groupe_01_ventes_ecommerce.csv` | 2 400 | 11 |
| **2** | Frindo Ilyass - Boushaba Zakariyae | Logistique & livraisons | `groupe_02_logistique_livraisons.csv` | 1 800 | 11 |
| **3** | Miguel KOUARA - SANOU Cedric A. Koudouss | Support client (tickets) | `groupe_03_support_client.csv` | 2 600 | 12 |
| **4** | Yahya BAKHRI-Taha HOUSNI | Ressources humaines | `groupe_04_ressources_humaines.csv` | 1 300 | 13 |
| **5** | Imane BAKKOU - Malak KENDOUSSI | Consommation énergétique | `groupe_05_energie_consommation.csv` | 2 900 | 11 |
| **6** | Meryem DAHBI-Sara YAZZOUGH | Transport urbain | `groupe_06_transport_urbain.csv` | 2 200 | 13 |
| **7** | Ben hassane Ibrahim - labib mohamed amine | Santé — consultations | `groupe_07_sante_consultations.csv` | 2 100 | 13 |
| **8** | Amr Aouame - khalil lahouiti | Agriculture — rendements | `groupe_08_agriculture_rendements.csv` | 1 600 | 13 |
| **9** | Salma Samadi - Aya Mriss | Tourisme & hôtellerie | `groupe_09_tourisme_hotellerie.csv` | 2 000 | 14 |
| **10** | Hamza kharbouch-Mounir Zarrouk | Banque — transactions | `groupe_10_banque_transactions.csv` | 3 000 | 13 |
| **11** | OUMMAHYA Chouaib- EL GADI Mouad | Industrie — production | `groupe_11_industrie_production.csv` | 1 900 | 14 |
| **12** | Taj Mariem - Rania Amezout | Télécom — trafic réseau | `groupe_12_telecom_reseau.csv` | 2 500 | 13 |
| **13** | abdellah karrouchi - DJIERE DATOUNI | Immobilier — annonces | `groupe_13_immobilier_annonces.csv` | 1 700 | 15 |
| **14** | salma azhar aya dghoghi | Éducation — résultats | `groupe_14_education_resultats.csv` | 2 300 | 14 |
| **15** | BENLAMINE Mohammed - OUTALEB Anwar | Stations-service carburant | `groupe_15_stations_carburant.csv` | 2 700 | 12 |
| **16** | Jamal eddine BOUHOUCH - Reda ISSAMI | Entrepôt — mouvements stock | `groupe_16_entrepot_stocks.csv` | 2 050 | 14 |
| **17** | Marwa Hablouk - Ikram Moudnibi | Qualité de l'air | `groupe_17_qualite_air.csv` | 2 800 | 14 |
| **18** | BOUA Meriame-CHBANI Rania | Mobilité VTC | `groupe_18_mobilite_vtc.csv` | 2 450 | 16 |

## Cahier des charges commun

Quel que soit le thème, le tableau de bord doit comporter :

1. **4 indicateurs clés (KPI)** en haut de page, qui réagissent aux filtres.
2. **4 graphiques** dont au moins une série temporelle et une comparaison par catégorie.
3. **3 filtres interactifs** minimum (`dcc.Dropdown`, `dcc.DatePickerRange`, `dcc.RadioItems`…)
   reliés à tous les graphiques par un `@callback`.
4. **Un tableau détaillé** (`dash.dash_table.DataTable`) paginé et triable.
5. **Une conclusion écrite** (2 à 3 phrases) répondant à la question d'analyse du groupe,
   chiffres à l'appui.

### Contraintes techniques

- Les données se chargent **une seule fois** au démarrage (hors fonction de callback).
- Aucune variable globale modifiée dans un callback : un callback lit, calcule, retourne.
- Les dates sont converties avec `pd.read_csv(..., parse_dates=[...])`.
- L'application tourne avec `python app.py` et s'ouvre sur `http://127.0.0.1:8050`.
- Un `README.md` dans le dossier du groupe : lancement, choix de conception, conclusion.

### Démarrage

```bash
python -m pip install dash plotly pandas
python tools/dash_starter.py --csv data/groupes/groupe_01_ventes_ecommerce.csv
```

`tools/dash_starter.py` est un squelette **générique et volontairement minimal** : il détecte
les colonnes, affiche un KPI, un graphique et un tableau. Il montre le câblage d'un callback —
il ne constitue pas le livrable.

---

## Briefs par groupe

### Groupe 01 — Ventes e-commerce

**Membres :** Choukri mohamed · Lassine Savani  
**Fichier :** `data/groupes/groupe_01_ventes_ecommerce.csv` — 2400 lignes × 11 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `commande_id` | texte | CMD-00001 |
| `date_commande` | date/heure | 2024-01-01 |
| `region` | texte | Fès |
| `canal` | texte | Mobile |
| `categorie` | texte | Audio |
| `produit` | texte | Micro USB |
| `prix_unitaire_mad` | décimal | 546.58 |
| `quantite` | entier | 1 |
| `remise_pct` | décimal | 0.0 |
| `chiffre_affaires_mad` | décimal | 546.58 |
| `statut` | texte | Livrée |

**KPI attendus :** Chiffre d'affaires total · Panier moyen · Taux d'annulation + retour

**Graphiques :**

1. CA mensuel (courbe)
2. CA par catégorie (barres triées)
3. CA par région et canal (barres empilées)
4. Top 10 produits (barres horizontales)

**Filtres :** période, région, canal, catégorie

**Question d'analyse :** Quel canal a la meilleure valeur de panier, et la remise accordée est-elle rentabilisée par le volume ?

> ⚠️ **Piège à éviter.** `chiffre_affaires_mad` vaut 0 pour les commandes annulées : ne divisez pas par le nombre de lignes brut pour le panier moyen.

---

### Groupe 02 — Logistique & livraisons

**Membres :** Frindo Ilyass · Boushaba Zakariyae  
**Fichier :** `data/groupes/groupe_02_logistique_livraisons.csv` — 1800 lignes × 11 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `livraison_id` | texte | LIV-00001 |
| `date_expedition` | date/heure | 2024-01-01 |
| `ville_depart` | texte | Casablanca |
| `ville_arrivee` | texte | Fès |
| `transporteur` | texte | SpeedLog |
| `poids_kg` | décimal | 54.33 |
| `distance_km` | décimal | 495.7 |
| `delai_promis_h` | décimal | 14.3 |
| `delai_reel_h` | décimal | 10.3 |
| `cout_mad` | décimal | 802.69 |
| `statut` | texte | À l'heure |

**KPI attendus :** Taux de livraison à l'heure · Délai moyen réel vs promis · Coût moyen au kilomètre

**Graphiques :**

1. Taux de ponctualité par transporteur (barres)
2. Délai réel vs distance (nuage)
3. Volume expédié par mois (courbe)
4. Coût moyen par axe ville_depart → ville_arrivee (heatmap)

**Filtres :** période, transporteur, ville de départ, statut

**Question d'analyse :** Quel transporteur est le moins cher à qualité de service égale ?

> ⚠️ **Piège à éviter.** Comparez `delai_reel_h` à `delai_promis_h`, qui dépend de la distance — un délai de 20 h n'est pas un retard sur 900 km.

---

### Groupe 03 — Support client (tickets)

**Membres :** Miguel KOUARA · SANOU Cedric A. Koudouss  
**Fichier :** `data/groupes/groupe_03_support_client.csv` — 2600 lignes × 12 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `ticket_id` | texte | TCK-00001 |
| `date_ouverture` | date/heure | 2025-01-01 07:00:00 |
| `canal` | texte | Téléphone |
| `categorie` | texte | Remboursement |
| `priorite` | texte | Haute |
| `agent` | texte | Y. Benjelloun |
| `sla_heures` | décimal | 8.0 |
| `premiere_reponse_min` | décimal | 14.3 |
| `temps_resolution_h` | décimal | 2.62 |
| `reouvertures` | entier | 0 |
| `satisfaction_1_5` | entier | 4 |
| `resolu` | booléen | True |

**KPI attendus :** Tickets ouverts · Taux de respect du SLA · Satisfaction moyenne

**Graphiques :**

1. Tickets par jour (courbe)
2. Respect du SLA par priorité (barres)
3. Charge par agent (barres)
4. Distribution du temps de résolution (histogramme)

**Filtres :** période, canal, catégorie, priorité, agent

**Question d'analyse :** Les tickets critiques sont-ils réellement traités en priorité, et au prix de quels autres tickets ?

> ⚠️ **Piège à éviter.** `sla_heures` varie selon la priorité : le respect du SLA se calcule ligne par ligne (`temps_resolution_h <= sla_heures`), pas sur une moyenne globale.

---

### Groupe 04 — Ressources humaines

**Membres :** Yahya BAKHRI · Taha HOUSNI  
**Fichier :** `data/groupes/groupe_04_ressources_humaines.csv` — 1300 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `employe_id` | texte | EMP-00001 |
| `departement` | texte | Logistique |
| `poste` | texte | Préparateur |
| `ville` | texte | Casablanca |
| `genre` | texte | F |
| `date_embauche` | date/heure | 2015-01-04 |
| `anciennete_mois` | décimal | 131.9 |
| `type_contrat` | texte | CDI |
| `salaire_mensuel_mad` | décimal | 4739.0 |
| `jours_absence_12m` | entier | 9 |
| `heures_formation_12m` | décimal | 3.6 |
| `score_evaluation` | décimal | 3.2 |
| `actif` | booléen | True |

**KPI attendus :** Effectif actif · Masse salariale mensuelle · Taux d'absentéisme

**Graphiques :**

1. Pyramide des salaires par département (boxplot ou barres)
2. Effectif par type de contrat (barres empilées)
3. Embauches par année (courbe)
4. Salaire vs ancienneté (nuage)

**Filtres :** département, ville, type de contrat, actif / inactif

**Question d'analyse :** À ancienneté et poste comparables, l'écart salarial entre `genre` est-il mesurable ?

> ⚠️ **Piège à éviter.** Filtrez `actif == True` pour la masse salariale : les inactifs ne sont plus payés.

---

### Groupe 05 — Consommation énergétique

**Membres :** Imane BAKKOU · Malak KENDOUSSI  
**Fichier :** `data/groupes/groupe_05_energie_consommation.csv` — 2900 lignes × 11 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `releve_id` | texte | REL-00001 |
| `horodatage` | date/heure | 2025-01-01 04:00:00 |
| `site` | texte | Entrepôt Berrechid |
| `compteur` | texte | C-04 |
| `usage` | texte | Process |
| `consommation_kwh` | décimal | 45.26 |
| `puissance_appelee_kw` | décimal | 56.27 |
| `tarif` | texte | Heures creuses |
| `prix_kwh_mad` | décimal | 0.78 |
| `cout_mad` | décimal | 35.3 |
| `temperature_ext_c` | décimal | 31.7 |

**KPI attendus :** Consommation totale (kWh) · Coût total (MAD) · Part consommée en heures de pointe

**Graphiques :**

1. Courbe de charge moyenne par heure (24 points)
2. Consommation par site et par usage (barres empilées)
3. Consommation mensuelle (courbe)
4. Consommation vs température extérieure (nuage)

**Filtres :** période, site, usage, tarif

**Question d'analyse :** Quelle part de la facture viendrait des heures de pointe, et quel usage faudrait-il décaler en heures creuses ?

> ⚠️ **Piège à éviter.** Le coût n'est pas proportionnel aux kWh : `prix_kwh_mad` double entre heures creuses et pointe. Agrégez `cout_mad`, pas `consommation_kwh × prix moyen`.

---

### Groupe 06 — Transport urbain

**Membres :** Meryem DAHBI · Sara YAZZOUGH  
**Fichier :** `data/groupes/groupe_06_transport_urbain.csv` — 2200 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `passage_id` | texte | PSG-00001 |
| `horodatage` | date/heure | 2025-09-01 00:00:00 |
| `ligne` | texte | L4 |
| `type_vehicule` | texte | Tramway |
| `station` | texte | Place des Nations |
| `sens` | texte | Aller |
| `periode` | texte | Heure normale |
| `passagers_montee` | entier | 18 |
| `passagers_descente` | entier | 19 |
| `capacite_vehicule` | entier | 220 |
| `taux_occupation_pct` | décimal | 25.2 |
| `retard_min` | décimal | 3.1 |
| `incident` | booléen | False |

**KPI attendus :** Passagers transportés · Taux d'occupation moyen · Retard moyen

**Graphiques :**

1. Fréquentation par heure (courbe, pointes du matin et du soir)
2. Taux d'occupation par ligne (barres)
3. Retard moyen par ligne et période (heatmap)
4. Top 10 stations par montées (barres horizontales)

**Filtres :** période, ligne, type de véhicule, sens, heure de pointe

**Question d'analyse :** Quelle ligne est saturée aux heures de pointe, et faut-il y ajouter un véhicule ou décaler les départs ?

> ⚠️ **Piège à éviter.** Un taux d'occupation > 100 % est normal (voyageurs debout) : ne le plafonnez pas à 100, c'est précisément le signal de saturation.

---

### Groupe 07 — Santé — consultations

**Membres :** Ben hassane Ibrahim · labib mohamed amine  
**Fichier :** `data/groupes/groupe_07_sante_consultations.csv` — 2100 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `consultation_id` | texte | CSL-00001 |
| `date_consultation` | date/heure | 2025-01-01 01:00:00 |
| `service` | texte | Chirurgie |
| `medecin` | texte | Dr Rachidi |
| `age_patient` | entier | 38 |
| `tranche_age` | texte | 30-44 |
| `genre` | texte | H |
| `mode_admission` | texte | Rendez-vous |
| `duree_attente_min` | décimal | 37.3 |
| `duree_consultation_min` | décimal | 45.9 |
| `actes_factures` | entier | 2 |
| `cout_mad` | décimal | 635.03 |
| `hospitalisation` | booléen | False |

**KPI attendus :** Consultations réalisées · Temps d'attente moyen · Taux d'hospitalisation

**Graphiques :**

1. Consultations par heure de la journée (courbe)
2. Attente moyenne par service (barres triées)
3. Répartition par tranche d'âge et genre (barres groupées)
4. Distribution du temps d'attente (histogramme)

**Filtres :** période, service, mode d'admission, tranche d'âge

**Question d'analyse :** Quel service fait attendre le plus longtemps, et l'attente est-elle due au volume ou à la durée des consultations ?

> ⚠️ **Piège à éviter.** La moyenne cache la queue de distribution : affichez aussi la médiane et le 90ᵉ percentile de `duree_attente_min`.

---

### Groupe 08 — Agriculture — rendements

**Membres :** Amr Aouame · khalil lahouiti  
**Fichier :** `data/groupes/groupe_08_agriculture_rendements.csv` — 1600 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `parcelle_id` | texte | PAR-00001 |
| `campagne` | texte | 2024-2025 |
| `date_recolte` | date/heure | 2023-01-06 |
| `region` | texte | Marrakech-Safi |
| `culture` | texte | Agrumes |
| `surface_ha` | décimal | 49.8 |
| `mode_irrigation` | texte | Aspersion |
| `pluviometrie_mm` | décimal | 503.1 |
| `rendement_t_ha` | décimal | 42.35 |
| `production_t` | décimal | 2109.03 |
| `prix_vente_mad_t` | décimal | 3128.71 |
| `revenu_mad` | décimal | 6457326.35 |
| `bio` | booléen | False |

**KPI attendus :** Production totale (t) · Rendement moyen (t/ha) · Revenu total (MAD)

**Graphiques :**

1. Rendement par culture (barres)
2. Rendement par mode d'irrigation (barres groupées)
3. Rendement vs pluviométrie (nuage avec tendance)
4. Production par région et campagne (barres empilées)

**Filtres :** campagne, région, culture, mode d'irrigation, bio

**Question d'analyse :** Le goutte-à-goutte se rentabilise-t-il, et sur quelles cultures l'écart de rendement est-il le plus net ?

> ⚠️ **Piège à éviter.** Ne faites jamais la moyenne de `rendement_t_ha` toutes cultures confondues : 95 t/ha de tomate et 3 t/ha de blé ne s'additionnent pas. Groupez d'abord par culture.

---

### Groupe 09 — Tourisme & hôtellerie

**Membres :** Salma Samadi · Aya Mriss  
**Fichier :** `data/groupes/groupe_09_tourisme_hotellerie.csv` — 2000 lignes × 14 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `reservation_id` | texte | RSV-00001 |
| `date_reservation` | date/heure | 2023-12-06 |
| `date_arrivee` | date/heure | 2024-01-01 |
| `ville` | texte | Marrakech |
| `categorie_etoiles` | entier | 3 |
| `canal_reservation` | texte | OTA |
| `nationalite` | texte | Maroc |
| `saison` | texte | Basse saison |
| `nuitees` | entier | 5 |
| `personnes` | entier | 2 |
| `prix_nuit_mad` | décimal | 648.19 |
| `montant_total_mad` | décimal | 3240.95 |
| `annulee` | booléen | False |
| `note_sejour` | décimal | 9.9 |

**KPI attendus :** Nuitées vendues · Revenu total · Taux d'annulation

**Graphiques :**

1. Nuitées par mois (saisonnalité)
2. Prix moyen par ville et catégorie (heatmap)
3. Répartition par nationalité (barres)
4. Revenu par canal de réservation (barres)

**Filtres :** période, ville, catégorie d'étoiles, canal, saison

**Question d'analyse :** Le canal OTA rapporte-t-il plus qu'il ne coûte en annulations, comparé à la réservation directe ?

> ⚠️ **Piège à éviter.** `montant_total_mad` vaut 0 si `annulee` : calculez le taux d'annulation sur le nombre de réservations, et le revenu sur les séjours honorés.

---

### Groupe 10 — Banque — transactions

**Membres :** Hamza kharbouch · Mounir Zarrouk  
**Fichier :** `data/groupes/groupe_10_banque_transactions.csv` — 3000 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `transaction_id` | texte | TRX-00001 |
| `horodatage` | date/heure | 2025-06-01 05:00:00 |
| `agence` | texte | Tanger Centre |
| `ville` | texte | Tanger |
| `type_operation` | texte | Retrait GAB |
| `canal` | texte | Mobile |
| `segment_client` | texte | Particulier |
| `devise` | texte | MAD |
| `montant_mad` | décimal | 245.0 |
| `frais_mad` | décimal | 2.94 |
| `solde_apres_mad` | décimal | 26958.15 |
| `score_risque` | décimal | 27.9 |
| `suspecte` | booléen | False |

**KPI attendus :** Volume total des transactions · Montant moyen · Nombre d'opérations suspectes

**Graphiques :**

1. Transactions par heure (pic diurne)
2. Montant par type d'opération (boxplot ou barres)
3. Répartition par canal et segment (barres empilées)
4. Score de risque vs montant (nuage, suspectes en évidence)

**Filtres :** période, agence, type d'opération, canal, segment

**Question d'analyse :** Les transactions suspectes se concentrent-elles sur un canal ou une plage horaire exploitable pour une règle d'alerte ?

> ⚠️ **Piège à éviter.** Les montants vont de 38 à 735 000 MAD : une échelle logarithmique, ou la médiane plutôt que la moyenne, est indispensable.

---

### Groupe 11 — Industrie — production

**Membres :** OUMMAHYA Chouaib · EL GADI Mouad  
**Fichier :** `data/groupes/groupe_11_industrie_production.csv` — 1900 lignes × 14 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `lot_id` | texte | LOT-00001 |
| `date_production` | date/heure | 2025-01-01 |
| `usine` | texte | Usine Berrechid |
| `ligne_production` | texte | L-C1 |
| `equipe` | texte | Équipe B (après-midi) |
| `reference_produit` | texte | REF-100 |
| `quantite_cible` | entier | 1500 |
| `quantite_produite` | entier | 1357 |
| `quantite_rebut` | entier | 27 |
| `taux_rebut_pct` | décimal | 1.97 |
| `duree_arret_min` | décimal | 33.0 |
| `trs_pct` | décimal | 89.53 |
| `cause_arret` | texte | Aucun |
| `conforme` | booléen | True |

**KPI attendus :** Quantité produite · Taux de rebut moyen · TRS moyen

**Graphiques :**

1. Production quotidienne vs cible (courbe double)
2. Taux de rebut par équipe (barres — l'équipe de nuit décroche)
3. Pareto des causes d'arrêt (barres triées + cumul)
4. TRS par ligne de production (barres)

**Filtres :** période, usine, ligne, équipe, référence produit

**Question d'analyse :** L'équipe de nuit produit-elle réellement plus de rebut, et pour quelle cause d'arrêt dominante ?

> ⚠️ **Piège à éviter.** Le taux de rebut global n'est pas la moyenne des taux par lot : c'est `somme(rebut) / somme(produite)`.

---

### Groupe 12 — Télécom — trafic réseau

**Membres :** Taj Mariem · Rania Amezout  
**Fichier :** `data/groupes/groupe_12_telecom_reseau.csv` — 2500 lignes × 13 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `session_id` | texte | SES-00001 |
| `horodatage` | date/heure | 2025-10-01 03:00:00 |
| `region` | texte | Casablanca-Settat |
| `technologie` | texte | 4G |
| `type_abonnement` | texte | Prépayé |
| `volume_data_mo` | décimal | 72.0 |
| `duree_appel_min` | décimal | 0.7 |
| `nb_sms` | entier | 2 |
| `latence_ms` | décimal | 47.0 |
| `debit_moyen_mbps` | décimal | 37.82 |
| `taux_echec_pct` | décimal | 2.53 |
| `revenu_session_mad` | décimal | 2.07 |
| `churn_risque` | booléen | False |

**KPI attendus :** Volume de données écoulé · Revenu total · Taux d'échec moyen

**Graphiques :**

1. Trafic par heure (courbe)
2. Latence par technologie (barres — 2G à 5G)
3. Répartition des sessions par technologie et région (barres empilées)
4. Revenu par type d'abonnement (barres)

**Filtres :** période, région, technologie, type d'abonnement

**Question d'analyse :** La 5G tient-elle sa promesse de latence partout, ou certaines régions restent-elles en retard ?

> ⚠️ **Piège à éviter.** La répartition des technologies est inégale (2G ≈ 5 % des sessions) : affichez l'effectif à côté de chaque moyenne, sinon la 2G paraît significative.

---

### Groupe 13 — Immobilier — annonces

**Membres :** abdellah karrouchi · DJIERE DATOUNI  
**Fichier :** `data/groupes/groupe_13_immobilier_annonces.csv` — 1700 lignes × 15 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `annonce_id` | texte | ANN-00001 |
| `date_publication` | date/heure | 2025-01-01 |
| `ville` | texte | Tanger |
| `quartier` | texte | Centre-ville |
| `type_bien` | texte | Local commercial |
| `transaction` | texte | Location |
| `surface_m2` | décimal | 99.5 |
| `nb_pieces` | entier | 4 |
| `etage` | entier | 6 |
| `annee_construction` | entier | 1981 |
| `prix_mad` | décimal | 5165.0 |
| `prix_m2_mad` | décimal | 51.91 |
| `ascenseur` | booléen | False |
| `jours_en_ligne` | entier | 24 |
| `vendu` | booléen | False |

**KPI attendus :** Annonces publiées · Prix moyen au m² · Taux de vente

**Graphiques :**

1. Prix au m² par ville (barres triées)
2. Prix vs surface (nuage par type de bien)
3. Annonces par quartier (barres horizontales, top 10)
4. Prix médian au m² par mois (courbe)

**Filtres :** ville, quartier, type de bien, transaction, période

**Question d'analyse :** Quels quartiers offrent le meilleur prix au m² à surface comparable ?

> ⚠️ **Piège à éviter.** PIÈGE CENTRAL : `prix_m2_mad` mélange un prix de vente et un loyer mensuel. Filtrez TOUJOURS sur `transaction` avant d'agréger cette colonne.

---

### Groupe 14 — Éducation — résultats

**Membres :** salma azhar aya dghoghi  
**Fichier :** `data/groupes/groupe_14_education_resultats.csv` — 2300 lignes × 14 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `evaluation_id` | texte | EVA-00001 |
| `annee_universitaire` | texte | 2025-2026 |
| `date_evaluation` | date/heure | 2023-10-02 |
| `filiere` | texte | Data & IA |
| `semestre` | texte | S2 |
| `module` | texte | Réseaux |
| `groupe_td` | texte | TD-3 |
| `genre` | texte | H |
| `note_cc` | décimal | 13.91 |
| `note_examen` | décimal | 13.6 |
| `note_finale` | décimal | 13.72 |
| `mention` | texte | Bien |
| `absences_heures` | entier | 3 |
| `admis` | booléen | True |

**KPI attendus :** Taux de réussite · Moyenne générale · Absentéisme moyen

**Graphiques :**

1. Distribution des notes finales (histogramme)
2. Moyenne par module (barres triées)
3. Taux de réussite par filière (barres)
4. Note finale vs absences (nuage avec tendance)

**Filtres :** année universitaire, filière, semestre, module, groupe de TD

**Question d'analyse :** L'absentéisme explique-t-il l'échec, et quel module tire la moyenne générale vers le bas ?

> ⚠️ **Piège à éviter.** `note_finale` = 0,4 × CC + 0,6 × examen : ne la recalculez pas comme une moyenne simple des deux notes.

---

### Groupe 15 — Stations-service carburant

**Membres :** BENLAMINE Mohammed · OUTALEB Anwar  
**Fichier :** `data/groupes/groupe_15_stations_carburant.csv` — 2700 lignes × 12 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `vente_id` | texte | VNT-00001 |
| `horodatage` | date/heure | 2025-01-01 02:00:00 |
| `station` | texte | Station Zenata |
| `ville` | texte | Casablanca |
| `pompe` | texte | P8 |
| `carburant` | texte | Gasoil |
| `type_client` | texte | Particulier |
| `volume_litres` | décimal | 26.88 |
| `prix_litre_mad` | décimal | 10.96 |
| `montant_mad` | décimal | 294.6 |
| `moyen_paiement` | texte | Carte carburant |
| `programme_fidelite` | booléen | False |

**KPI attendus :** Volume vendu (litres) · Chiffre d'affaires · Panier moyen par passage

**Graphiques :**

1. Ventes par heure (courbe)
2. Volume par carburant (barres)
3. CA par station (barres triées)
4. Prix du litre dans le temps (courbe par carburant)

**Filtres :** période, station, carburant, type de client, moyen de paiement

**Question d'analyse :** Les clients flotte et poids lourd justifient-ils une pompe dédiée dans certaines stations ?

> ⚠️ **Piège à éviter.** Un poids lourd prend 180 L, un particulier 28 L : séparez le volume (litres) du nombre de passages, sinon la fréquentation est illisible.

---

### Groupe 16 — Entrepôt — mouvements stock

**Membres :** Jamal eddine BOUHOUCH · Reda ISSAMI  
**Fichier :** `data/groupes/groupe_16_entrepot_stocks.csv` — 2050 lignes × 14 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `mouvement_id` | texte | MVT-00002 |
| `date_mouvement` | date/heure | 2025-01-01 |
| `entrepot` | texte | Entrepôt Casablanca |
| `zone` | texte | B |
| `sku` | texte | SKU-BRI-302 |
| `categorie` | texte | Bricolage |
| `fournisseur` | texte | Sahara Distrib |
| `type_mouvement` | texte | Entrée |
| `quantite` | entier | 16 |
| `stock_apres` | entier | 353 |
| `stock_mini` | entier | 45 |
| `valeur_unitaire_mad` | décimal | 1244.5 |
| `valeur_mouvement_mad` | décimal | 19912.0 |
| `rupture` | booléen | False |

**KPI attendus :** Valeur du stock · Nombre de références en rupture · Taux de rotation

**Graphiques :**

1. Niveau de stock dans le temps pour une référence (courbe + seuil `stock_mini`)
2. Valeur immobilisée par catégorie (barres)
3. Entrées vs sorties par mois (barres groupées)
4. Références sous le seuil mini (tableau conditionnel)

**Filtres :** période, entrepôt, zone, catégorie, SKU, type de mouvement

**Question d'analyse :** Quelles références passent le plus souvent sous le seuil mini, et faut-il relever leur point de commande ?

> ⚠️ **Piège à éviter.** `quantite` est signée (négative en sortie) : une somme brute donne le flux net, pas le volume manipulé — utilisez la valeur absolue pour l'activité.

---

### Groupe 17 — Qualité de l'air

**Membres :** Marwa Hablouk · Ikram Moudnibi  
**Fichier :** `data/groupes/groupe_17_qualite_air.csv` — 2800 lignes × 14 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `mesure_id` | texte | AIR-00001 |
| `horodatage` | date/heure | 2025-01-01 00:00:00 |
| `ville` | texte | Casablanca |
| `station` | texte | Urbaine centre |
| `pm25_ug_m3` | décimal | 23.5 |
| `pm10_ug_m3` | décimal | 35.8 |
| `no2_ug_m3` | décimal | 29.4 |
| `o3_ug_m3` | décimal | 35.8 |
| `so2_ug_m3` | décimal | 1.1 |
| `temperature_c` | décimal | 7.8 |
| `humidite_pct` | décimal | 46.4 |
| `vent_kmh` | décimal | 4.8 |
| `indice_aqi` | entier | 68 |
| `categorie_aqi` | texte | Modéré |

**KPI attendus :** AQI moyen · Jours au-delà du seuil OMS (PM2.5 > 15) · Polluant dominant

**Graphiques :**

1. AQI moyen par ville (barres triées)
2. Profil horaire des PM2.5 (courbe, pics de trafic)
3. Répartition des catégories AQI (barres empilées par ville)
4. PM2.5 vs vitesse du vent (nuage — la dispersion)

**Filtres :** période, ville, type de station, catégorie AQI

**Question d'analyse :** Les pics de pollution sont-ils dus aux émissions (heures de pointe) ou à l'absence de vent ?

> ⚠️ **Piège à éviter.** Les données sont horaires : un seuil journalier de l'OMS doit se comparer à une moyenne sur 24 h, obtenue par `resample('D')`.

---

### Groupe 18 — Mobilité VTC

**Membres :** BOUA Meriame · CHBANI Rania  
**Fichier :** `data/groupes/groupe_18_mobilite_vtc.csv` — 2450 lignes × 16 colonnes

| Colonne | Type | Exemple |
|---|---|---|
| `course_id` | texte | CRS-00001 |
| `horodatage_commande` | date/heure | 2025-07-01 03:00:00 |
| `ville` | texte | Rabat |
| `zone_depart` | texte | Résidentiel |
| `zone_arrivee` | texte | Zone industrielle |
| `gamme` | texte | Confort |
| `chauffeur_id` | texte | DRV-00051 |
| `attente_min` | décimal | 0.9 |
| `distance_km` | décimal | 5.59 |
| `duree_min` | décimal | 15.1 |
| `coefficient_surge` | décimal | 1.0 |
| `tarif_mad` | décimal | 31.16 |
| `pourboire_mad` | décimal | 1.06 |
| `moyen_paiement` | texte | Portefeuille app |
| `note_chauffeur` | décimal | 5.0 |
| `annulee` | booléen | False |

**KPI attendus :** Courses réalisées · Recette totale · Taux d'annulation

**Graphiques :**

1. Courses par heure (courbe, pics nocturnes)
2. Recette moyenne par gamme (barres)
3. Flux zone de départ → zone d'arrivée (heatmap)
4. Tarif vs distance (nuage, coloré par coefficient de surge)

**Filtres :** période, ville, gamme, zone de départ, moyen de paiement

**Question d'analyse :** Le surge appliqué correspond-il aux heures où l'attente des clients est réellement la plus longue ?

> ⚠️ **Piège à éviter.** `tarif_mad` et `pourboire_mad` valent 0 pour les courses annulées : excluez `annulee == True` de toute moyenne de recette.

---

## Note pour l'encadrant

Les jeux de données sont **synthétiques et reproductibles** : la graine aléatoire dérive du
numéro de groupe, donc `python tools/gen_group_datasets.py` régénère des fichiers identiques
au bit près. Un groupe ne peut pas être pénalisé par un nouveau tirage.

Chaque jeu contient un signal réel à trouver (saisonnalité, heures de pointe, un écart entre
équipes ou entre canaux) et un piège d'agrégation documenté ci-dessus — c'est là que se fait
la différence entre un tableau de bord qui affiche et un tableau de bord qui explique.

Régénérer un seul groupe : `python tools/gen_group_datasets.py --groupes 7`
