import pandas as pd

animaux = pd.read_csv("filtre_donnees_animaux/bdc_18_01.csv", sep=",", on_bad_lines="skip", dtype=str)
animaux94 = pd.read_csv("filtre_donnees_animaux/fauneflore_94.csv", sep=";", on_bad_lines="skip", dtype=str)

animaux["LB_NOM"] = animaux["LB_NOM"].str.strip().str.lower()
animaux94["NomLatinAppelTaxon"] = animaux94["NomLatinAppelTaxon"].str.strip().str.lower()

codes_94 = animaux94["NomLatinAppelTaxon"].tolist()

filtered_df = animaux[animaux["LB_NOM"].isin(codes_94)]

print(f"Filtered {len(filtered_df)} rows out of {len(animaux)}")
filtered_df.to_csv("filtre_donnees_animaux/animaux_protege_94.csv", sep=";", index=False)

filtered_df["LB_NOM"] = filtered_df["LB_NOM"].str.strip().str.lower()
animaux94["NomLatinAppelTaxon"] = animaux94["NomLatinAppelTaxon"].str.strip().str.lower()


merged = animaux94.merge(
    filtered_df,
    left_on="NomLatinAppelTaxon",
    right_on="LB_NOM",
    how="left"
)


colonnes_a_supprimer = [
    "LB_NOM",         
    "THEMATIQUE",
    "TYPE_VALUE",
    "NOM_COMPLET_HTML",
    "NOM_VALIDE_HTML",
    "CD_ISO3166_2",
    "FULL_CITATION",
    "DOC_URL"
]
merged = merged.drop(columns=colonnes_a_supprimer, errors="ignore")

print(f"Lignes : {len(merged)}")
print(f"Colonnes : {merged.columns.tolist()}")
print(merged.head(3))

merged.to_csv("filtre_donnees_animaux/fauneflore_94_protege.csv", sep=";", index=False)
