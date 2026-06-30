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

def euclidean_distance(x1, y1, x2, y2):
    try:
        x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    except (ValueError, TypeError):
        return float('inf')
    distance_metres = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance_metres / 1000.0

@app.get("/station-proche")
def get_station_proche(lat_user: float, lon_user: float):

    conn = sqlite3.connect("naiades_database.db")
    conn.create_function("EUC_DIST", 4, euclidean_distance)
    cursor = conn.cursor()
    
    user_x_lambert, user_y_lambert = transformer.transform(lon_user, lat_user)

    try:
        query = """
            SELECT LbStationMesureEauxSurface, CoordXStationMesureEauxSurface, CoordYStationMesureEauxSurface, EUC_DIST(?, ?, CoordXStationMesureEauxSurface, CoordYStationMesureEauxSurface) AS distance
            FROM Stations
            WHERE CoordXStationMesureEauxSurface IS NOT NULL 
              AND CoordYStationMesureEauxSurface IS NOT NULL
            ORDER BY distance ASC
            LIMIT 1;
        """

        cursor.execute(query, (user_x_lambert, user_y_lambert))
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
            "lambert_x": float(result[1]),
            "lambert_y": float(result[2]),
            "distance_km": round(result[3], 2),
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)