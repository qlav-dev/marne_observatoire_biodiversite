from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pyproj import Transformer
import math
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)

@app.get("/stations-zone")
def get_stations_zone(lat1: float, lon1: float, lat2: float, lon2: float):
    
    x1, y1 = transformer.transform(lon1, lat1)
    x2, y2 = transformer.transform(lon2, lat2)

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    conn = sqlite3.connect("naiades_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        query = """
            SELECT LbStationMesureEauxSurface AS nom, 
                   CoordXStationMesureEauxSurface AS lambert_x, 
                   CoordYStationMesureEauxSurface AS lambert_y
            FROM Stations
            WHERE CoordXStationMesureEauxSurface IS NOT NULL
              AND CAST(CoordXStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
              AND CAST(CoordYStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
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
        stations.append({
            "nom": row["nom"],
            "lambert_x": float(row["lambert_x"]),
            "lambert_y": float(row["lambert_y"])
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

@app.get("/station-infos")
def get_station_infos(nom_station: str):
    conn = sqlite3.connect("naiades_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # On utilise LIKE pour chercher une correspondance partielle
        query = """
            SELECT * FROM Stations 
            WHERE LbStationMesureEauxSurface LIKE ? 
            LIMIT 1;
        """
        
        cursor.execute(query, (f"%{nom_station}%",))
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
            detail=f"Aucune station trouvée contenant le nom : '{nom_station}'"
        )

    return {
        "station_infos": dict(result)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)