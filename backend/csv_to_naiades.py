import sqlite3
import pandas as pd
import os

dossier_actuel = os.path.dirname(os.path.abspath(__file__))

fichier_csv = os.path.join(dossier_actuel, "ammonium.csv")
nom_base_donnees = "eau_database.db"
nom_table = "Ammonium" # Le nom de la table que tu cibles

# 2. Connexion à la base SQLite
conn = sqlite3.connect(nom_base_donnees)

try:
    print("Lecture du fichier CSV en cours...")
    df = pd.read_csv(fichier_csv, sep=',', encoding='utf-8')
    
    print(f"Fichier lu avec succès : {len(df)} lignes trouvées.")
    print("Insertion dans la base de données...")

    df.to_sql(nom_table, conn, if_exists='append', index=False)
    
    print(f"Succès ! Les données ont été insérées dans la table '{nom_table}'.")

except FileNotFoundError:
    print(f"Erreur : Le fichier {fichier_csv} est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")

finally:
    # 5. Fermeture de la connexion (très important !)
    conn.close()
    print("Connexion à la base de données fermée.")