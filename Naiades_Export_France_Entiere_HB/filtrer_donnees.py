import pandas as pd

stations = pd.read_csv("Naiades_Export_France_Entiere_HB/stations.csv", sep=";", on_bad_lines="skip", dtype=str)
stations94 = stations[stations["CodeDepartement"] == "94"]
stations94["CdStationMesureEauxSurface"] = pd.to_numeric(stations94["CdStationMesureEauxSurface"], errors='coerce').astype('Int64')

station_codes = stations94["CdStationMesureEauxSurface"].tolist()

fichiers = ["resultat", "operation", "fauneflore", "cep"]

for x in fichiers:
    print(f"loading {x}")
    df = pd.read_csv(f"Naiades_Export_France_Entiere_HB/{x}.csv", sep=";", on_bad_lines="skip", dtype=str)
    df["CdStationMesureEauxSurface"] = pd.to_numeric(df["CdStationMesureEauxSurface"], errors='coerce').astype('Int64')
    print(df["CdStationMesureEauxSurface"], stations94["CdStationMesureEauxSurface"])
    
    filtered_df = df[df["CdStationMesureEauxSurface"].isin(station_codes)]
    
    print(f"Filtered {len(filtered_df)} rows out of {len(df)}")
    print(f"exporting {x}")
    
    # Save with appropriate separator and without index
    filtered_df.to_csv(f"Naiades_Export_France_Entiere_HB/{x}_94.csv", sep=";", index=False)