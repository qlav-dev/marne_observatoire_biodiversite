
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Stations;

CREATE TABLE IF NOT EXISTS Stations (
    CdStationMesureEauxSurface INTEGER
    LbStationMesureEauxSurface TEXT
    DurStationMesureEauxSurface TEXT
    CoordXStationMesureEauxSurface REAL
    CoordYStationMesureEauxSurface REAL
    CdProjStationMesureEauxSurface INTEGER
    LibelleProjection TEXT
    CodeCommune INTEGER
    LbCommune TEXT
    CodeDepartement INTEGER 
    LbDepartement TEXT
    CodeRegion INTEGER
    LbRegion TEXT
    CdMasseDEau INTEGER
    CdEuMasseDEau INTEGER
    NomMasseDEau TEXT
    CdEuSsBassinDCEAdmin INTEGER    
    NomSsBassinDCEAdmin TEXT
    CdBassinDCE INTEGER
    CdEuBassinDCE INTEGER
    NomEuBassinDCE TEXT
    CdTronconHydrographique TEXT
    CdCoursdEau TEXT
    NomCoursdEau TEXT
    CodeTypEthStationMesureEauxSurface INTEGER
    LibelleTypEthStationMesureEauxSurface   TEXT
    ComStationMesureEauxSurface TEXT
    DateCreationStationMesureEauxSurface TEXT    
    DateArretActiviteStationMesureEauxSurface TEXT   
    DateMAJInfosStationMesureEauxSurface TEXT
    FinaliteStationMesureEauxSurface TEXT
    LocPreciseStationMesureEauxSurface TEXT
    CodeNatureStationMesureEauxSurface  INTEGER
    LibelleNatureStationMesureEauxSurface   TEXT
    AltitudePointCaracteritisque INTEGER
    PkPointTronconEntiteHydroPrincipale REAL 
    PremierMoisAnneeEtiage  REAL 
    SuperficieBassinVersantReel REAL 
    SuperficieBassinVersantTopo REAL 

);


-- Index pour meilleur performances
CREATE INDEX IF NOT EXISTS idx_stations_support ON Stations(CdSupport);
CREATE INDEX IF NOT EXISTS idx_stations_taxon ON Stations(CdAppelTaxon);
CREATE INDEX IF NOT EXISTS idx_stations_producteur ON Stations(CdProducteur);
CREATE INDEX IF NOT EXISTS idx_stations_date ON Stations(DateDebutOperationPrelBio);

-- View pour des colonnes plus lisibles
CREATE VIEW IF NOT EXISTS v_Stations AS
SELECT 
    CdStationMesureEauxSurface AS StationId,
    LbStationMesureEauxSurface AS StationName,
    CdSupport AS SupportId,
    LbSupport AS SupportLabel,
    DateDebutOperationPrelBio AS OperationStartDate,
    CdAppelTaxon AS TaxonId,
    NomLatinAppelTaxon AS TaxonLatinName,
    RsTaxRep AS TaxRepValue,
    CdProducteur AS ProducerId,
    NomProducteur AS ProducerName
FROM Stations;