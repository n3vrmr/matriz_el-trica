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

ax = sns.barplot(final_1,x="Value",y="Area",hue="Year",palette="Spectral_r")
ax.set_title(
    "Participação de fontes de energia renovável na matriz elétrica dos países"
    )
ax.set_xlabel("Valor em %")
ax.set_xlim(right=100)
ax.set_ylabel("País")
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


def main():
    if __name__ == '__main__':
        print("Qual é a dificuldade de usar os dados certos, Poder360?")
    return

main()

