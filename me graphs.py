# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:04:18 2025

@author: Nevermore
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv("yearly_full_release_long_format.csv")

past_two_years = dataset[dataset["Year"] >= 2023]

country_list = ["Brazil","Canada","Germany","Spain","United Kingdom","Italy",
                "EU","Turkey","Australia","Argentina","China","Japan","France",
                "United States of America","India","Mexico",
                "Russian Federation (the)","South Africa","South Korea"]

def top_ecos(data):
    df_list = []
    for country in country_list:
        country_df = data[data["Area"] == country]
        df_list.append(country_df)
    
    top_ecos_df = pd.concat(df_list)
    
    return top_ecos_df

top = top_ecos(past_two_years)

# energy_source = top["Variable"].value_counts()

esp = top[top["Unit"] == "%"]

# Alôoooo Poder 360, era só fazer isso pra ter os números corretos kkkkkk
renewables = esp[esp["Variable"] == "Renewables"]

def portuguese_names(data):

    data.loc[data["Area"] == "Brazil", "Area"] = "Brasil"
    data.loc[data["Area"] == "Canada", "Area"] = "Canadá"
    data.loc[data["Area"] == "Germany", "Area"] = "Alemanha"
    data.loc[data["Area"] == "Spain", "Area"] = "Espanha"
    data.loc[data["Area"] == "United Kingdom", "Area"] = "Reino Unido"
    data.loc[data["Area"] == "Italy", "Area"] = "Itália"
    data.loc[data["Area"] == "EU", "Area"] = "União Europeia"
    data.loc[data["Area"] == "Turkey", "Area"] = "Turquia"
    data.loc[data["Area"] == "Australia", "Area"] = "Austrália"
    data.loc[data["Area"] == "Japan", "Area"] = "Japão"
    data.loc[data["Area"] == "France", "Area"] = "França"
    data.loc[data["Area"] == "United States of America", "Area"] = "EUA"
    data.loc[data["Area"] == "India", "Area"] = "Índia"
    data.loc[data["Area"] == "Mexico", "Area"] = "México"
    data.loc[data["Area"] == "Russian Federation (the)", "Area"] = "Rússia"
    data.loc[data["Area"] == "South Africa", "Area"] = "África do Sul"
    data.loc[data["Area"] == "South Korea", "Area"] = "Coreia do Sul"
    
    return data

renewables_ptbr = portuguese_names(renewables)

renewables_ptbr = renewables_ptbr.drop(labels=
                                       ["Country code","Area type","Continent",
                                        "Ember region","EU","OECD","G20","G7",
                                        "ASEAN","Category","Subcategory",
                                        "Variable","Unit","YoY absolute change"
                                        ], axis=1).reset_index(drop=True)

for i in range(0,37):
    if (i+1) % 2 != 0:
        renewables_ptbr.iloc[
            i+1,3] = renewables_ptbr.iloc[i+1,2] - renewables_ptbr.iloc[i,2]
    else:
        pass

final_1 = renewables_ptbr
country_names = final_1["Area"].value_counts()
countries = list(country_names.index)

# list comprehension go brr
new_df = pd.DataFrame({"País":countries,
                       "2023":[float(
                           final_1.iloc[i,2]
                           ) for i in range(0,38) if i % 2 == 0],
                       "2024":[float(
                           final_1.iloc[i+1,2]
                           ) for i in range(0,38) if i % 2 == 0],
                       "Variação em p. p.":
                           [float(
                               final_1.iloc[i+1,3]
                               ) for i in range(0,38) if i % 2 == 0]})

new_df.to_excel("Tabela 1.xlsx")

ax = sns.barplot(final_1,x="Value",y="Area",hue="Year",palette="winter")
ax.set_title(
    "Total de fontes de Energia Renovável na Matriz Elétrica dos países"
    , fontsize=18, pad=15)
ax.set_xlabel("Valor em %")
ax.set_xlim(right=100)
ax.set_ylabel("País")
ax.legend(title="Ano")
plt.show()

# now for the second graph (Poder360, if you are reading this: get on my level)

esp_fuel = esp[esp["Subcategory"] == "Fuel"]
esp_fuel_2024 = esp_fuel[esp_fuel["Year"] == 2024]

espf_2024_ptbr = portuguese_names(esp_fuel_2024)
espf_24_reduced = espf_2024_ptbr.drop(labels=
                                       ["Country code","Area type","Continent",
                                        "Ember region","EU","OECD","G20","G7",
                                        "ASEAN","Category","Subcategory",
                                        "Unit","YoY absolute change"
                                        ], axis=1).reset_index(drop=True)

# Os dados não incluem energia nuclear gerada pela Austrália, por algum motivo
# Pra não dar merda depois, é melhor adicionar uma linha agora

espf_24_reduced.loc[72.5] = ["Austrália",2024,"Nuclear",0,np.nan]
espf_24_reduced = espf_24_reduced.sort_index().reset_index(drop=True)

def ptbr_energysource(data):
    
    data.loc[data["Variable"] == "Bioenergy", "Variable"] = "Bioenergia"
    data.loc[data["Variable"] == "Coal", "Variable"] = "Carvão"
    data.loc[data["Variable"] == "Gas", "Variable"] = "Gás"
    data.loc[data["Variable"] == "Hydro", "Variable"] = "Hidráulica"
    data.loc[data["Variable"] == "Other Fossil", "Variable"] = "Outras fósseis"
    data.loc[data["Variable"] == "Wind", "Variable"] = "Eólica"
    data.loc[data["Variable"] == "Other Renewables",
             "Variable"] = "Outras renováveis"
    
    return data

espf24r_ptbr = ptbr_energysource(espf_24_reduced).reset_index(drop=True)

def sum_sources(data):
    
    data.loc[data["Variable"] == "Bioenergia",
             "Variable"] = "Outras renováveis"
    data.loc[data["Variable"] == "Solar",
             "Variable"] = "Solar e eólica"
    data.loc[data["Variable"] == "Eólica",
             "Variable"] = "Solar e eólica"
    
    data_sum = data.groupby(["Area","Variable"], as_index=False,
                            sort=False)["Value"].sum()
    
    return data_sum

summed_sources = sum_sources(espf24r_ptbr)

paises = list(espf24r_ptbr["Area"].value_counts(sort=False).index)

# There's probably a better way to do this...
brasil = summed_sources[summed_sources["Area"] == "Brasil"]
canada = summed_sources[summed_sources["Area"] == "Canadá"].reset_index(
    drop=True)
alemanha = summed_sources[summed_sources["Area"] == "Alemanha"].reset_index(
    drop=True)
espanha = summed_sources[summed_sources["Area"] == "Espanha"].reset_index(
    drop=True)
uk = summed_sources[summed_sources["Area"] == "Reino Unido"].reset_index(
    drop=True)
italia = summed_sources[summed_sources["Area"] == "Itália"].reset_index(
    drop=True)
ue = summed_sources[summed_sources[
    "Area"] == "União Europeia"].reset_index(drop=True)
turquia = summed_sources[summed_sources["Area"] == "Turquia"].reset_index(
    drop=True)
australia = summed_sources[summed_sources[
    "Area"] == "Austrália"].reset_index(drop=True)
argentina = summed_sources[summed_sources[
    "Area"] == "Argentina"].reset_index(drop=True)
china = summed_sources[summed_sources["Area"] == "China"].reset_index(
    drop=True)
japao = summed_sources[summed_sources["Area"] == "Japão"].reset_index(
    drop=True)
franca = summed_sources[summed_sources["Area"] == "França"].reset_index(
    drop=True)
eua = summed_sources[summed_sources["Area"] == "EUA"].reset_index(
    drop=True)
india = summed_sources[summed_sources["Area"] == "Índia"].reset_index(
    drop=True)
mexico = summed_sources[summed_sources["Area"] == "México"].reset_index(
    drop=True)
russia = summed_sources[summed_sources["Area"] == "Rússia"].reset_index(
    drop=True)
africadosul = summed_sources[summed_sources[
    "Area"] == "África do Sul"].reset_index(drop=True)
coreiadosul = summed_sources[summed_sources[
    "Area"] == "Coreia do Sul"].reset_index(drop=True)

category_names = ['Hidráulica', 'Solar e eólica', 'Outras renováveis',
                  'Carvão','Gás','Outras fósseis','Nuclear']

# Below is just copied from matplotlib's barh example

values_percent = {
    'Brasil': [float
               (brasil[brasil["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Canadá': [float
               (canada[canada["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Alemanha': [float
               (alemanha[alemanha["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Espanha': [float
               (espanha[espanha["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Reino Unido': [float
               (uk[uk["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Itália': [float
               (italia[italia["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'União Europeia': [float
               (ue[ue["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Turquia': [float
               (turquia[turquia["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Austrália': [float
               (australia[australia["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Argentina': [float
               (argentina[argentina["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'China': [float
               (china[china["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Japão': [float
               (japao[japao["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'França': [float
               (franca[franca["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'EUA': [float
               (eua[eua["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Índia': [float
               (india[india["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'México': [float
               (mexico[mexico["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Rússia': [float
               (russia[russia["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'África do Sul': [float
               (africadosul[africadosul["Variable"] == i].iloc[0,2]
                ) for i in category_names],
    'Coreia do Sul': [float
               (coreiadosul[coreiadosul["Variable"] == i].iloc[0,2]
                ) for i in category_names]}


def graph(values_percent, category_names):
    """
    Parameters
    ----------
    values_percent : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(values_percent.keys())
    data = np.array(list(values_percent.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['terrain'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.set_title("Composição da Matriz Elétrica dos países (2024)", fontsize=18,
                 pad=30)
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    ax.set_xlabel("Participação da fonte de energia elétrica em %")

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        # ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(-0.05, 1),
              loc='lower left', fontsize='small')

    return fig, ax


graph(values_percent, category_names)
plt.show()

def main():
    if __name__ == '__main__':
        print("Qual é a dificuldade de NÃO USAR IA PRA FAZER ISSO, Poder360?")
    return

main()

