from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pyproj import Transformer
from typing import Optional
import math
import sqlite3

DATABASE_PATH = "database.db"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend React
        "http://127.0.0.1:3000",
        # Pour le développement, vous pouvez utiliser "*" mais pas en production
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Autorise tous les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

# Transformer for Lambert to Lat/Lng
transformer_to_lambert = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
transformer_to_lambert = Transformer.from_crs(
    "EPSG:4326", "EPSG:2154", always_xy=True)
# Transformer for Lat/Lng to Lambert (inverse)
transformer_to_wgs84 = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
transformer_to_wgs84 = Transformer.from_crs(
    "EPSG:2154", "EPSG:4326", always_xy=True)


def get_db_connection():
    conn = sqlite3.connect("naiades_database.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.get("/stations-zone")
def get_stations_zone(lat1: float, lon1: float, lat2: float, lon2: float):
    

    x1, y1 = transformer_to_lambert.transform(lon1, lat1)
    x2, y2 = transformer_to_lambert.transform(lon2, lat2)

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    conn = sqlite3.connect("naiades_database.db")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        query = """
            SELECT LbStationMesureEauxSurface AS nom, 
                    CoordXStationMesureEauxSurface AS lambert_x, 
                    CoordYStationMesureEauxSurface AS lambert_y,
                    CdStationMesureEauxSurface AS CdStationMesureEauxSurface
            FROM Stations
            WHERE CoordXStationMesureEauxSurface IS NOT NULL
            AND CAST(CoordXStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
            AND CAST(CoordYStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
            AND CodeDepartement = '94'
        """
        

        cursor.execute(query, (min_x, max_x, min_y, max_y))
        results = cursor.fetchall()

    except sqlite3.OperationalError as e:
        conn.close()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur SQL. Erreur : {e}",
        )

    conn.close()

    stations = []
    for row in results:
        # Convert Lambert to Lat/Lng for each station
        lon, lat = transformer_to_wgs84.transform(
            float(row["lambert_x"]), 
            float(row["lambert_x"]),
            float(row["lambert_y"])
        )
        stations.append({
            "nom": row["nom"],
            "lambert_x": float(row["lambert_x"]),
            "lambert_y": float(row["lambert_y"]),
            "latitude": lat,
            "longitude": lon,
            "code":  row["CdStationMesureEauxSurface"]
        })

    return {
        "metadonnees": {
            "nombre_stations_trouvees": len(stations),
            "zone_lambert93": {
                "x_min": round(min_x, 2), "x_max": round(max_x, 2),
                "y_min": round(min_y, 2), "y_max": round(max_y, 2)
            }
        },
        "stations": stations
    }


@app.get("/station-observations")
def get_station_observations(code_station: int):
    conn = sqlite3.connect("naiades_database.db")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        query = """
            SELECT * FROM Operations WHERE CdStationMesureEauxSurface = ? ORDER BY DateDebutOperationPrelBio DESC
        """

        cursor.execute(query, (code_station, ))
        result = cursor.fetchall()

    except sqlite3.OperationalError as e:
        conn.close()
        raise HTTPException(
            status_code=500,
            detail = f"Erreur SQL"
            detail=f"Erreur SQL"
        )
    

    conn.close()

    if not result:
        raise HTTPException(
            status_code=500,
            detail = f"Erreur SQL"
            detail=f"Erreur SQL"
        )

    return result


@app.get("/station-infos")
def get_station_infos(code_station: int):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # On utilise LIKE pour chercher une correspondance partielle
        query = """
            SELECT * FROM Stations 
            WHERE CdStationMesureEauxSurface = ?
            LIMIT 1;
        """

        cursor.execute(query, (code_station,))
        result = cursor.fetchone()

    except sqlite3.OperationalError as e:
        conn.close()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur SQL. Vérifie le nom de tes colonnes ! Erreur : {e}",
        )

    conn.close()

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune station trouvée ayant le code : '{code_station}'"
        )

    station_dict = dict(result)
    if station_dict.get('CoordXStationMesureEauxSurface') and station_dict.get('CoordYStationMesureEauxSurface'):
        lon, lat = transformer_to_wgs84.transform(
            float(station_dict['CoordXStationMesureEauxSurface']),
            float(station_dict['CoordYStationMesureEauxSurface'])
        )
        station_dict['latitude'] = lat
        station_dict['longitude'] = lon

    return {
        "station_infos": station_dict
    }

# New endpoint to convert Lambert coordinates to Lat/Lng
@app.get("/convert-lambert-to-latlng")
def convert_lambert_to_latlng(x: float, y: float):
    """
    Convert Lambert 93 coordinates (EPSG:2154) to WGS84 (EPSG:4326)
    """
    try:
        lon, lat = transformer_to_wgs84.transform(x, y)
        return {
            "lambert_x": x,
            "lambert_y": y,
            "latitude": lat,
            "longitude": lon
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de conversion: {str(e)}"
        )

# New endpoint to convert Lat/Lng to Lambert
@app.get("/convert-latlng-to-lambert")
def convert_latlng_to_lambert(lat: float, lng: float):
    """
    Convert WGS84 (EPSG:4326) to Lambert 93 coordinates (EPSG:2154)
    """
    try:
        x, y = transformer_to_lambert.transform(lng, lat)
        return {
            "latitude": lat,
            "longitude": lng,
            "lambert_x": x,
            "lambert_y": y
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de conversion: {str(e)}"
        )
    


@app.get("/station-animaux-evolution")
def get_station_animaux_evolution(code_station: int, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        query = f"""
            SELECT 
                DateDebutOperationPrelBio AS date_mesure,
                NomLatinAppelTaxon AS espece_latin,
                LbListeFauFlor AS espece_commun,
                SUM(CAST(RsTaxRep AS REAL)) AS abondance,
                SymUniteMesure AS unite,
                LABEL_STATUT AS statut_protection
            FROM AnimauxProteges
            WHERE CdStationMesureEauxSurface = ? 
              AND RsTaxRep IS NOT NULL 
              AND DateDebutOperationPrelBio IS NOT NULL
            GROUP BY DateDebutOperationPrelBio, NomLatinAppelTaxon
            ORDER BY DateDebutOperationPrelBio ASC;
        """
        cursor.execute(query, (code_station,))
        results = cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du croisement des données : {e}. Vérifie tes tables.")

    if not results:
        return {
            "code_station": code_station,
            "message": "Aucun recensement d'animal protégé répertorié à cette station.",
            "donnees_evolution": []
        }

    # 3. Structuration de l'historique chronologique pour le graphique du site
    historique = []
    liste_especes_presentes = set()
    
    for row in results:
        liste_especes_presentes.add(row["espece_latin"])
        historique.append({
            "date": row["date_mesure"],
            "espece_latin": row["espece_latin"],
            "espece_commun": row["espece_commun"] if row["espece_commun"] else "Inconnu",
            "abondance": row["abondance"],
            "unite": row["unite"] if row["unite"] else "individus",
            "statut_protection": row["statut_protection"]
        })

    return {
        "metadonnees": {
            "code_station": code_station,
            "total_especes_protegees_trouvees": len(liste_especes_presentes),
            "liste_especes": list(liste_especes_presentes)
        },
        "donnees_evolution": historique
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)