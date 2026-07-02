"""
API Naiades - Service de données sur les stations de mesure d'eau
Version: 1.0.0

Tout à été refactor par Deepseek, merci à lui
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pyproj import Transformer
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import sqlite3
import logging
from dataclasses import dataclass
from enum import Enum

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ CONFIGURATION ============


class Config:
    DATABASE_PATH = "database.db"
    EAU_DATABASE_PATH = "eau_database.db"
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    DEPARTMENT_CODE = '94'  # Val-de-Marne

# ============ MODÈLES DE DONNÉES ============


@dataclass
class Station:
    """Modèle de station de mesure"""
    nom: str
    lambert_x: float
    lambert_y: float
    latitude: float
    longitude: float
    code: str


@dataclass
class Observation:
    """Modèle d'observation"""
    date: str
    parametre: str
    valeur: float
    unite: str


@dataclass
class ZoneGeographique:
    """Modèle de zone géographique"""
    x_min: float
    x_max: float
    y_min: float
    y_max: float

# ============ GESTIONNAIRE DE BASE DE DONNÉES ============


class DatabaseManager:
    """Gestionnaire de connexions à la base de données"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """Context manager pour les connexions SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception as e:
            logger.error(f"Erreur de base de données: {e}")
            raise
        finally:
            conn.close()

# ============ SERVICE DE CONVERSION ============


class CoordinateService:
    """Service de conversion de coordonnées géographiques"""

    def __init__(self):
        # Transformer pour Lambert vers WGS84
        self.to_wgs84 = Transformer.from_crs(
            "EPSG:2154", "EPSG:4326", always_xy=True)
        # Transformer pour WGS84 vers Lambert
        self.to_lambert = Transformer.from_crs(
            "EPSG:4326", "EPSG:2154", always_xy=True)

    def lambert_to_wgs84(self, x: float, y: float) -> tuple:
        """Convertit les coordonnées Lambert 93 en WGS84"""
        try:
            lon, lat = self.to_wgs84.transform(x, y)
            return lat, lon
        except Exception as e:
            raise ValueError(f"Erreur de conversion Lambert->WGS84: {e}")

    def wgs84_to_lambert(self, lat: float, lon: float) -> tuple:
        """Convertit les coordonnées WGS84 en Lambert 93"""
        try:
            x, y = self.to_lambert.transform(lon, lat)
            return x, y
        except Exception as e:
            raise ValueError(f"Erreur de conversion WGS84->Lambert: {e}")

# ============ SERVICE DE STATIONS ============


class StationService:
    """Service de gestion des stations"""

    def __init__(self, db_manager: DatabaseManager, coord_service: CoordinateService):
        self.db_manager = db_manager
        self.coord_service = coord_service

    def get_stations_in_zone(self, lat1: float, lon1: float, lat2: float, lon2: float) -> List[Station]:
        """Récupère les stations dans une zone géographique"""
        try:
            # Conversion des coordonnées en Lambert
            x1, y1 = self.coord_service.wgs84_to_lambert(lat1, lon1)
            x2, y2 = self.coord_service.wgs84_to_lambert(lat2, lon2)

            # Définition de la zone
            zone = ZoneGeographique(
                x_min=min(x1, x2),
                x_max=max(x1, x2),
                y_min=min(y1, y2),
                y_max=max(y1, y2)
            )

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT 
                        LbStationMesureEauxSurface AS nom,
                        CoordXStationMesureEauxSurface AS lambert_x,
                        CoordYStationMesureEauxSurface AS lambert_y,
                        CdStationMesureEauxSurface AS code
                    FROM Stations
                    WHERE CoordXStationMesureEauxSurface IS NOT NULL
                        AND CAST(CoordXStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
                        AND CAST(CoordYStationMesureEauxSurface AS REAL) BETWEEN ? AND ?
                        AND CodeDepartement = ?
                """
                cursor.execute(query, (zone.x_min, zone.x_max,
                               zone.y_min, zone.y_max, Config.DEPARTMENT_CODE))
                results = cursor.fetchall()

            # Construction des objets Station
            stations = []
            for row in results:
                lat, lon = self.coord_service.lambert_to_wgs84(
                    float(row["lambert_x"]),
                    float(row["lambert_y"])
                )
                stations.append(Station(
                    nom=row["nom"],
                    lambert_x=float(row["lambert_x"]),
                    lambert_y=float(row["lambert_y"]),
                    latitude=lat,
                    longitude=lon,
                    code=row["code"]
                ))

            return stations

        except Exception as e:
            logger.error(f"Erreur dans get_stations_in_zone: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération des stations: {e}")

    def get_station_info(self, code_station: int) -> Dict[str, Any]:
        """Récupère les informations d'une station spécifique"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT * FROM Stations 
                    WHERE CdStationMesureEauxSurface = ?
                    LIMIT 1
                """
                cursor.execute(query, (code_station,))
                result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404, detail=f"Station {code_station} non trouvée")

            station_dict = dict(result)

            # Ajout des coordonnées géographiques
            if station_dict.get('CoordXStationMesureEauxSurface') and station_dict.get('CoordYStationMesureEauxSurface'):
                lat, lon = self.coord_service.lambert_to_wgs84(
                    float(station_dict['CoordXStationMesureEauxSurface']),
                    float(station_dict['CoordYStationMesureEauxSurface'])
                )
                station_dict['latitude'] = lat
                station_dict['longitude'] = lon

            return station_dict

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur dans get_station_info: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération des informations: {e}")

# ============ SERVICE D'OBSERVATIONS ============


class ObservationService:
    """Service de gestion des observations"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_station_observations(self, code_station: int) -> List[Dict[str, Any]]:
        """Récupère les observations d'une station"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT * FROM Operations 
                    WHERE CdStationMesureEauxSurface = ? 
                    ORDER BY DateDebutOperationPrelBio DESC
                """
                cursor.execute(query, (code_station,))
                results = cursor.fetchall()

            if not results:
                raise HTTPException(
                    status_code=404, detail=f"Aucune observation pour la station {code_station}")

            return [dict(row) for row in results]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur dans get_station_observations: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération des observations: {e}")

    def get_station_animal_evolution(self, code_station: int) -> Dict[str, Any]:
        """Récupère l'évolution des espèces animales à une station"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT 
                        DateDebutOperationPrelBio AS date_mesure,
                        NomLatinAppelTaxon AS espece_latin,
                        LbListeFauFlor AS espece_commun,
                        SUM(CAST(RsTaxRep AS REAL)) AS abondance,
                        SymUniteMesure AS unite,
                        LABEL_STATUT AS statut_protection
                    FROM Operations
                    WHERE CdStationMesureEauxSurface = ? 
                        AND RsTaxRep IS NOT NULL 
                        AND DateDebutOperationPrelBio IS NOT NULL
                    GROUP BY DateDebutOperationPrelBio, NomLatinAppelTaxon
                    ORDER BY DateDebutOperationPrelBio ASC
                """
                cursor.execute(query, (code_station,))
                results = cursor.fetchall()

            if not results:
                return {
                    "code_station": code_station,
                    "message": "Aucun recensement d'animal protégé répertorié à cette station",
                    "donnees_evolution": []
                }

            # Traitement des données
            historique = []
            especes = set()

            for row in results:
                row_dict = dict(row)
                especes.add(row_dict["espece_latin"])
                historique.append({
                    "date": row_dict["date_mesure"],
                    "espece_latin": row_dict["espece_latin"],
                    "espece_commun": row_dict["espece_commun"] or "Inconnu",
                    "abondance": float(row_dict["abondance"]) if row_dict["abondance"] else 0,
                    "unite": row_dict["unite"] or "individus",
                    "statut_protection": row_dict["statut_protection"]
                })

            return {
                "metadonnees": {
                    "code_station": code_station,
                    "total_especes_protegees_trouvees": len(especes),
                    "liste_especes": list(especes)
                },
                "donnees_evolution": historique
            }

        except Exception as e:
            logger.error(f"Erreur dans get_station_animal_evolution: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération des données: {e}")

# ============ SERVICE EAU ============


class EauService:
    """Service pour les données de qualité de l'eau"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_station_eau_evolution(self, code_station: int) -> Dict[str, Any]:
        """Récupère l'évolution des paramètres de qualité de l'eau"""
        parametres = ["ammonium", "DBO5", "temperature"]
        resultats = {}

        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                for parametre in parametres:
                    query = f"""
                        SELECT DatePrel AS date_prelevement, 
                               RsAna AS resultat, 
                               SymUniteMesure AS unite
                        FROM {parametre}
                        WHERE CdStationMesureEauxSurface = ? 
                            AND RsAna IS NOT NULL 
                            AND DatePrel IS NOT NULL
                        ORDER BY DatePrel ASC
                    """
                    cursor.execute(query, (code_station,))
                    resultats[parametre] = [dict(row)
                                            for row in cursor.fetchall()]

            return {
                "code_station": code_station,
                "parametres": resultats
            }

        except sqlite3.OperationalError as e:
            logger.error(f"Erreur SQL dans get_station_eau_evolution: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur de base de données: {e}")
        except Exception as e:
            logger.error(f"Erreur dans get_station_eau_evolution: {e}")
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération des données: {e}")


# ============ INITIALISATION DE L'APPLICATION ============
app = FastAPI(
    title="API Naiades",
    description="API pour les données des stations de mesure d'eau",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des services
db_manager = DatabaseManager(Config.DATABASE_PATH)
eau_db_manager = DatabaseManager(Config.EAU_DATABASE_PATH)
coord_service = CoordinateService()
station_service = StationService(db_manager, coord_service)
observation_service = ObservationService(db_manager)
eau_service = EauService(eau_db_manager)

# ============ ENDPOINTS ============


@app.get("/")
async def root():
    """Endpoint racine avec documentation des services disponibles"""
    return {
        "message": "API Naiades - Stations de mesure",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/stations-zone", "method": "GET",
                "description": "Récupère les stations dans une zone"},
            {"path": "/station-observations", "method": "GET",
                "description": "Récupère les observations d'une station"},
            {"path": "/station-infos", "method": "GET",
                "description": "Récupère les informations d'une station"},
            {"path": "/convert-lambert-to-latlng", "method": "GET",
                "description": "Convertit Lambert vers WGS84"},
            {"path": "/convert-latlng-to-lambert", "method": "GET",
                "description": "Convertit WGS84 vers Lambert"},
            {"path": "/station-animaux-evolution", "method": "GET",
                "description": "Évolution des espèces animales"},
            {"path": "/station-eau-evolution", "method": "GET",
                "description": "Évolution de la qualité de l'eau"}
        ]
    }


@app.get("/stations-zone")
async def get_stations_zone(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Récupère les stations dans une zone géographique définie par deux points
    """
    try:
        stations = station_service.get_stations_in_zone(lat1, lon1, lat2, lon2)

        return {
            "metadonnees": {
                "nombre_stations_trouvees": len(stations),
                "zone_lambert93": {
                    "x_min": min(s.lambert_x for s in stations) if stations else 0,
                    "x_max": max(s.lambert_x for s in stations) if stations else 0,
                    "y_min": min(s.lambert_y for s in stations) if stations else 0,
                    "y_max": max(s.lambert_y for s in stations) if stations else 0
                }
            },
            "stations": [
                {
                    "nom": s.nom,
                    "lambert_x": s.lambert_x,
                    "lambert_y": s.lambert_y,
                    "latitude": s.latitude,
                    "longitude": s.longitude,
                    "code": s.code
                }
                for s in stations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/station-observations")
async def get_station_observations(code_station: int):
    """Récupère toutes les observations d'une station"""
    return observation_service.get_station_observations(code_station)


@app.get("/station-infos")
async def get_station_infos(code_station: int):
    """Récupère les informations détaillées d'une station"""
    station_info = station_service.get_station_info(code_station)
    return {"station_infos": station_info}


@app.get("/convert-lambert-to-latlng")
async def convert_lambert_to_latlng(x: float, y: float):
    """Convertit des coordonnées Lambert 93 en WGS84"""
    try:
        lat, lon = coord_service.lambert_to_wgs84(x, y)
        return {
            "lambert_x": x,
            "lambert_y": y,
            "latitude": lat,
            "longitude": lon
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/convert-latlng-to-lambert")
async def convert_latlng_to_lambert(lat: float, lng: float):
    """Convertit des coordonnées WGS84 en Lambert 93"""
    try:
        x, y = coord_service.wgs84_to_lambert(lat, lng)
        return {
            "latitude": lat,
            "longitude": lng,
            "lambert_x": x,
            "lambert_y": y
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/station-animaux-evolution")
async def get_station_animaux_evolution(code_station: int):
    """Récupère l'évolution des espèces animales à une station"""
    return observation_service.get_station_animal_evolution(code_station)


@app.get("/station-eau-evolution")
async def get_station_eau_evolution(code_station: int):
    """Récupère l'évolution de la qualité de l'eau à une station"""
    return eau_service.get_station_eau_evolution(code_station)

# ============ GESTIONNAIRE D'ERREURS ============


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestionnaire personnalisé des exceptions HTTP"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {"error": exc.detail, "status_code": exc.status_code}


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gestionnaire des exceptions générales"""
    logger.error(f"Exception non gérée: {exc}")
    return {"error": "Une erreur interne est survenue", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
