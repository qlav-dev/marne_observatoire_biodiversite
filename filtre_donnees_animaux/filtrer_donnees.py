import pandas as pd

animaux = pd.read_csv("filtre_donnees_animaux/bdc_18_01.csv", sep=",", on_bad_lines="skip", dtype=str)
animaux94 = pd.read_csv("filtre_donnees_animaux/fauneflore_94.csv", sep=";", on_bad_lines="skip", dtype=str)

animaux["LB_NOM"] = animaux["LB_NOM"].str.strip().str.lower()
animaux94["NomLatinAppelTaxon"] = animaux94["NomLatinAppelTaxon"].str.strip().str.lower()

codes_94 = animaux94["NomLatinAppelTaxon"].tolist()

filtered_df = animaux[animaux["LB_NOM"].isin(codes_94)]

print(f"Filtered {len(filtered_df)} rows out of {len(animaux)}")
filtered_df.to_csv("filtre_donnees_animaux/animaux_protege_94.csv", sep=";", index=False)
