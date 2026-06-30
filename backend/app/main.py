from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
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

def haversine_distance(lat1, lon1, lat2, lon2):

    try:
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    except (ValueError, TypeError):
        return float('inf')

    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.get("/station-proche")
def get_station_proche(lat_user: float, lon_user: float):

    conn = sqlite3.connect("naiades_database.db")
    conn.create_function("HA_DIST", 4, haversine_distance)
    cursor = conn.cursor()

    try:
        query = """
            SELECT LbStationMesureEauxSurface, CoordYStationMesureEauxSurface, CoordXStationMesureEauxSurface, HA_DIST(?, ?, CoordYStationMesureEauxSurface, CoordXStationMesureEauxSurface) AS distance
            FROM Stations
            WHERE CoordXStationMesureEauxSurface IS NOT NULL 
            AND CoordYStationMesureEauxSurface IS NOT NULL
            ORDER BY distance ASC
            LIMIT 1;
        """

        cursor.execute(query, (lat_user, lon_user))
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
            status_code=404, detail="Aucune station trouvée dans la base."
        )

    # On structure la réponse JSON propre
    return {
        "station_la_plus_proche": {
            "nom": result[0],
            "latitude": result[1],
            "longitude": result[2],
            "distance_km": round(result[3], 2),
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)