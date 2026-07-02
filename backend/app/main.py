"""
API Naiades - Service de données sur les stations de mesure d'eau
Version: 2.0.0 - Version simplifiée
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyproj import Transformer
from contextlib import contextmanager
import sqlite3
import logging
from typing import List, Dict, Any

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ CONFIGURATION ============
DATABASE_PATH = "database.db"
EAU_DATABASE_PATH = "eau_database.db"
DEPARTMENT_CODE = '94'

# ============ BASE DE DONNÉES ============
@contextmanager
def get_db(db_path: str):
    """Connexion à la base de données"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def execute_query(db_path: str, query: str, params: tuple = ()):
    """Exécute une requête et retourne les résultats"""
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_table_columns(db_path: str, table_name: str) -> List[str]:
    """Récupère la liste des colonnes d'une table"""
    query = f"PRAGMA table_info({table_name})"
    results = execute_query(db_path, query)
    return [row['name'] for row in results]

# ============ COORDONNÉES ============
class CoordConverter:
    """Conversion de coordonnées"""
    def __init__(self):
        self.to_wgs84 = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
        self.to_lambert = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
    
    def lambert_to_wgs84(self, x: float, y: float):
        lon, lat = self.to_wgs84.transform(x, y)
        return lat, lon
    
    def wgs84_to_lambert(self, lat: float, lon: float):
        return self.to_lambert.transform(lon, lat)

converter = CoordConverter()

# ============ FONCTIONS MÉTIER ============
def get_stations_in_zone(lat1: float, lon1: float, lat2: float, lon2: float) -> List[Dict]:
    """Récupère les stations dans une zone"""
    x1, y1 = converter.wgs84_to_lambert(lat1, lon1)
    x2, y2 = converter.wgs84_to_lambert(lat2, lon2)
    
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    
    query = """
        SELECT 
            LbStationMesureEauxSurface AS nom,
            CoordXStationMesureEauxSurface AS x,
            CoordYStationMesureEauxSurface AS y,
            CdStationMesureEauxSurface AS code
        FROM Stations
        WHERE CoordXStationMesureEauxSurface IS NOT NULL
            AND CAST(CoordXStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
            AND CAST(CoordYStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
            AND CodeDepartement = ?
    """
    
    results = execute_query(DATABASE_PATH, query, (x_min, x_max, y_min, y_max, DEPARTMENT_CODE))
    
    stations = []
    for row in results:
        lat, lon = converter.lambert_to_wgs84(float(row['x']), float(row['y']))
        stations.append({
            "nom": row['nom'],
            "code": row['code'],
            "latitude": lat,
            "longitude": lon,
            "lambert_x": float(row['x']),
            "lambert_y": float(row['y'])
        })
    
    return stations

def get_station_info(code_station: int) -> Dict:
    """Informations d'une station"""
    query = "SELECT * FROM Stations WHERE CdStationMesureEauxSurface = ? LIMIT 1"
    result = execute_query(DATABASE_PATH, query, (code_station,))
    
    if not result:
        raise HTTPException(404, f"Station {code_station} non trouvée")
    
    data = dict(result[0])
    if data.get('CoordXStationMesureEauxSurface') and data.get('CoordYStationMesureEauxSurface'):
        lat, lon = converter.lambert_to_wgs84(
            float(data['CoordXStationMesureEauxSurface']),
            float(data['CoordYStationMesureEauxSurface'])
        )
        data['latitude'] = lat
        data['longitude'] = lon
    
    return data

def get_observations(code_station: int) -> List[Dict]:
    """Observations d'une station"""
    # Récupérer les colonnes disponibles
    columns = get_table_columns(DATABASE_PATH, "Operations")
    
    query = f"""
        SELECT *
        FROM Operations 
        WHERE CdStationMesureEauxSurface = ? 
        ORDER BY DateDebutOperationPrelBio DESC
    """
    
    results = execute_query(DATABASE_PATH, query, (code_station,))
    
    if not results:
        raise HTTPException(404, f"Aucune observation pour la station {code_station}")
    
    return [dict(row) for row in results]

def get_animal_evolution(code_station: int) -> Dict:
    """Évolution des espèces animales"""
    try:
        # Récupérer les colonnes disponibles
        columns = get_table_columns(DATABASE_PATH, "AnimauxProteges")
        
        # Vérifier que la colonne existe
        if "NomLatinAppelTaxon" not in columns:
            return {
                "code_station": code_station,
                "message": "Colonne 'NomLatinAppelTaxon' non trouvée",
                "especes": [],
                "evolution": []
            }
        
        # Construction de la requête
        query = """
            SELECT *
            FROM AnimauxProteges
            WHERE CdStationMesureEauxSurface = ?
        """
        
        results = execute_query(DATABASE_PATH, query, (code_station,))
        
    except sqlite3.OperationalError as e:
        logger.error(f"Erreur SQL: {e}")
        return {
            "code_station": code_station,
            "message": f"Erreur lors de la requête: {str(e)}",
            "especes": [],
            "evolution": []
        }
    
    if not results:
        return {
            "code_station": code_station,
            "message": "Aucune espèce protégée recensée",
            "especes": [],
            "evolution": []
        }
    
    # Extraire les espèces uniques
    nom_latin_index = columns.index("NomLatinAppelTaxon")
    especes = list(set([x[nom_latin_index] for x in results]))
    
    # Organiser les données par espèce
    especes_data = {}
    for row in results:
        espece = row[nom_latin_index]
        if espece not in especes_data:
            especes_data[espece] = []
        
        # Convertir la ligne en dictionnaire avec les noms de colonnes
        row_dict = {columns[i]: row[i] for i in range(len(columns))}
        especes_data[espece].append(row_dict)
    
    return {
        "code_station": code_station,
        "liste_especes": especes,
        "evolution": especes_data,
    }

def get_eau_evolution(code_station: int) -> Dict:
    """Évolution de la qualité de l'eau"""
    # Récupérer les colonnes de la table eau
    try:
        columns = get_table_columns(EAU_DATABASE_PATH, "ammonium")
    except:
        return {
            "code_station": code_station,
            "message": "Base de données eau non disponible",
            "parametres": {}
        }
    
    # Vérifier les colonnes disponibles
    has_date = 'DatePrel' in columns
    has_result = 'RsAna' in columns
    has_unite = 'SymUniteMesure' in columns
    
    if not has_date or not has_result:
        return {
            "code_station": code_station,
            "message": "Colonnes nécessaires non disponibles",
            "parametres": {}
        }
    
    parametres = ["ammonium", "DBO5", "temperature"]
    resultats = {}
    
    for parametre in parametres:
        try:
            # Vérifier si la table existe
            cols = get_table_columns(EAU_DATABASE_PATH, parametre)
            if not cols:
                continue
                
            select_parts = ['DatePrel AS date']
            if 'RsAna' in cols:
                select_parts.append('RsAna AS valeur')
            if 'SymUniteMesure' in cols:
                select_parts.append('SymUniteMesure AS unite')
            
            query = f"""
                SELECT {', '.join(select_parts)}
                FROM {parametre}
                WHERE CdStationMesureEauxSurface = ? 
                    AND RsAna IS NOT NULL 
                    AND DatePrel IS NOT NULL
                ORDER BY DatePrel ASC
            """
            resultats[parametre] = [dict(row) for row in execute_query(EAU_DATABASE_PATH, query, (code_station,))]
        except sqlite3.OperationalError:
            # La table n'existe probablement pas
            resultats[parametre] = []
    
    return {
        "code_station": code_station,
        "parametres": resultats
    }

# ============ APPLICATION FASTAPI ============
app = FastAPI(title="API Naiades", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ ENDPOINTS ============
@app.get("/")
async def root():
    return {
        "message": "API Naiades",
        "version": "2.0.0",
        "endpoints": [
            "/stations-zone?lat1=&lon1=&lat2=&lon2=",
            "/station-infos?code_station=",
            "/station-observations?code_station=",
            "/station-animaux-evolution?code_station=",
            "/station-eau-evolution?code_station=",
            "/convert-lambert-to-latlng?x=&y=",
            "/convert-latlng-to-lambert?lat=&lng="
        ]
    }

@app.get("/stations-zone")
async def stations_zone(lat1: float, lon1: float, lat2: float, lon2: float):
    try:
        stations = get_stations_in_zone(lat1, lon1, lat2, lon2)
        return {
            "total": len(stations),
            "stations": stations
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/station-infos")
async def station_infos(code_station: int):
    return get_station_info(code_station)

@app.get("/station-observations")
async def station_observations(code_station: int):
    return get_observations(code_station)

@app.get("/station-animaux-evolution")
async def animaux_evolution(code_station: int):
    return get_animal_evolution(code_station)

@app.get("/station-eau-evolution")
async def eau_evolution(code_station: int):
    return get_eau_evolution(code_station)

@app.get("/convert-lambert-to-latlng")
async def convert_lambert(x: float, y: float):
    lat, lon = converter.lambert_to_wgs84(x, y)
    return {"lambert_x": x, "lambert_y": y, "latitude": lat, "longitude": lon}

@app.get("/convert-latlng-to-lambert")
async def convert_latlng(lat: float, lng: float):
    x, y = converter.wgs84_to_lambert(lat, lng)
    return {"latitude": lat, "longitude": lng, "lambert_x": x, "lambert_y": y}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)