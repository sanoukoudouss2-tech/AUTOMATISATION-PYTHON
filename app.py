"""Dashboard Dash — Support client (groupe 3).

Lancement : python app.py  ->  http://127.0.0.1:8050
Prérequis : calculs.py dans le même dossier, et le CSV au chemin CHEMIN_CSV
(data/groupes/groupe_03_support_client.csv), ou adaptez CHEMIN_CSV dans calculs.py.
"""

import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html

from calculs import (
    charger_donnees,
    charge_par_agent,
    filtrer,
    nb_tickets,
    nb_tickets_non_resolus,
    premiere_reponse_moyenne,
    satisfaction_moyenne,
    sla_par_priorite,
    stats_par_priorite,
    taux_sla,
    temps_resolution,
    tickets_par_jour,
)

# ----------------------------------------------------------------------
# Données : chargées UNE SEULE FOIS, hors de tout callback
# ----------------------------------------------------------------------
df = charger_donnees()

DATE_MIN = df["date_ouverture"].min().date()
DATE_MAX = df["date_ouverture"].max().date()
OPT_CANAL = sorted(df["canal"].dropna().unique())
OPT_CATEGORIE = sorted(df["categorie"].dropna().unique())
OPT_AGENT = sorted(df["agent"].dropna().unique())
OPT_PRIORITE = list(sla_par_priorite(df)["priorite"])  # déjà dans l'ordre voulu

# À REMPLIR à la fin, avec vos chiffres (2 à 3 phrases) : elle s'affiche en bas de page
# et doit aussi figurer dans le README.md du groupe.
CONCLUSION = (
    "À rédiger : répondez à la question « Les tickets critiques sont-ils réellement "
    "traités en priorité, et au prix de quels autres tickets ? » en citant les chiffres "
    "du tableau de synthèse par priorité."
)

# ----------------------------------------------------------------------
# Mise en page
# ----------------------------------------------------------------------
STYLE_CARTE = {
    "flex": "1", "minWidth": "180px", "padding": "14px", "textAlign": "center",
    "border": "1px solid #ddd", "borderRadius": "8px", "background": "#fafafa",
}


def carte_kpi(id_valeur, titre):
    return html.Div([
        html.Div(titre, style={"fontSize": "13px", "color": "#555"}),
        html.Div("—", id=id_valeur, style={"fontSize": "28px", "fontWeight": "bold"}),
    ], style=STYLE_CARTE)


def filtre(libelle, composant):
    return html.Div([html.Label(libelle, style={"fontWeight": "bold"}), composant],
                    style={"flex": "1", "minWidth": "200px"})


app = Dash(__name__)
app.title = "Support client — Groupe 3"

app.layout = html.Div([
    html.H1("Tableau de bord — Support client"),

    # Filtres
    html.Div([
        filtre("Période", dcc.DatePickerRange(
            id="f-periode", min_date_allowed=DATE_MIN, max_date_allowed=DATE_MAX,
            start_date=DATE_MIN, end_date=DATE_MAX, display_format="DD/MM/YYYY")),
        filtre("Canal", dcc.Dropdown(OPT_CANAL, multi=True, id="f-canal",
                                     placeholder="Tous les canaux")),
        filtre("Catégorie", dcc.Dropdown(OPT_CATEGORIE, multi=True, id="f-categorie",
                                         placeholder="Toutes les catégories")),
        filtre("Priorité", dcc.Dropdown(OPT_PRIORITE, multi=True, id="f-priorite",
                                        placeholder="Toutes les priorités")),
        filtre("Agent", dcc.Dropdown(OPT_AGENT, multi=True, id="f-agent",
                                     placeholder="Tous les agents")),
    ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "margin": "16px 0"}),

    # KPI
    html.Div([
        carte_kpi("kpi-tickets", "Tickets ouverts"),
        carte_kpi("kpi-sla", "Respect du SLA"),
        carte_kpi("kpi-satisfaction", "Satisfaction moyenne (/5)"),
        carte_kpi("kpi-reponse", "1re réponse moyenne (min)"),
    ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

    # Graphiques
    html.Div([
        html.Div(dcc.Graph(id="g-jour"), style={"flex": "1", "minWidth": "420px"}),
        html.Div(dcc.Graph(id="g-sla"), style={"flex": "1", "minWidth": "420px"}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginTop": "16px"}),
    html.Div([
        html.Div(dcc.Graph(id="g-agent"), style={"flex": "1", "minWidth": "420px"}),
        html.Div(dcc.Graph(id="g-hist"), style={"flex": "1", "minWidth": "420px"}),
    ], style={"display": "flex", "flexWrap": "wrap"}),

    # Synthèse par priorité (aide à la conclusion)
    html.H3("Synthèse par priorité"),
    dash_table.DataTable(id="t-synthese", style_cell={"textAlign": "center"},
                         style_header={"fontWeight": "bold"}),

    # Tableau détaillé : paginé et triable
    html.H3("Détail des tickets"),
    dash_table.DataTable(
        id="t-detail", page_size=15, page_action="native", sort_action="native",
        style_table={"overflowX": "auto"}, style_cell={"textAlign": "left", "padding": "4px"},
        style_header={"fontWeight": "bold"},
    ),

    # Conclusion
    html.H3("Conclusion"),
    html.P(CONCLUSION, id="conclusion"),
], style={"maxWidth": "1300px", "margin": "0 auto", "padding": "16px",
          "fontFamily": "sans-serif"})


# ----------------------------------------------------------------------
# Callback unique : lit les filtres, calcule, retourne (aucune globale modifiée)
# ----------------------------------------------------------------------
def fmt(valeur, decimales=1, suffixe=""):
    return "—" if valeur is None else f"{valeur:.{decimales}f}{suffixe}"


@callback(
    Output("kpi-tickets", "children"),
    Output("kpi-sla", "children"),
    Output("kpi-satisfaction", "children"),
    Output("kpi-reponse", "children"),
    Output("g-jour", "figure"),
    Output("g-sla", "figure"),
    Output("g-agent", "figure"),
    Output("g-hist", "figure"),
    Output("t-synthese", "data"),
    Output("t-synthese", "columns"),
    Output("t-detail", "data"),
    Output("t-detail", "columns"),
    Input("f-periode", "start_date"),
    Input("f-periode", "end_date"),
    Input("f-canal", "value"),
    Input("f-categorie", "value"),
    Input("f-priorite", "value"),
    Input("f-agent", "value"),
)
def mettre_a_jour(debut, fin, canaux, categories, priorites, agents):
    d = filtrer(df, debut, fin, canaux, categories, priorites, agents)

    # KPI
    k_tickets = f"{nb_tickets(d):,}".replace(",", " ")
    k_sla = fmt(taux_sla(d), 1, " %")
    k_satisfaction = fmt(satisfaction_moyenne(d), 2)
    k_reponse = fmt(premiere_reponse_moyenne(d), 1)

    # Graphiques
    fig_jour = px.line(tickets_par_jour(d), x="date", y="tickets",
                       title="Tickets ouverts par jour",
                       labels={"date": "Date", "tickets": "Tickets"})

    fig_sla = px.bar(sla_par_priorite(d), x="priorite", y="taux_sla_pct",
                     title="Respect du SLA par priorité",
                     labels={"priorite": "Priorité", "taux_sla_pct": "SLA respecté (%)"})
    fig_sla.update_yaxes(range=[0, 100])

    fig_agent = px.bar(charge_par_agent(d), x="agent", y="tickets",
                       title="Charge par agent",
                       labels={"agent": "Agent", "tickets": "Tickets"})

    fig_hist = px.histogram(temps_resolution(d), nbins=40,
                            title="Distribution du temps de résolution",
                            labels={"value": "Temps de résolution (h)", "count": "Tickets"})
    fig_hist.update_layout(showlegend=False, yaxis_title="Tickets")

    # Synthèse par priorité
    synthese = stats_par_priorite(d).reset_index()
    col_synthese = [{"name": c, "id": c} for c in synthese.columns]

    # Tableau détaillé (dates et booléens convertis pour l'affichage)
    detail = d.drop(columns=["sla_respecte"]).copy()
    detail["date_ouverture"] = detail["date_ouverture"].dt.strftime("%Y-%m-%d %H:%M")
    detail["resolu"] = detail["resolu"].astype(str)
    col_detail = [{"name": c, "id": c} for c in detail.columns]

    return (k_tickets, k_sla, k_satisfaction, k_reponse,
            fig_jour, fig_sla, fig_agent, fig_hist,
            synthese.to_dict("records"), col_synthese,
            detail.to_dict("records"), col_detail)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)