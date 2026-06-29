
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Stations;

CREATE TABLE IF NOT EXISTS Stations (
    CdStationMesureEauxSurface   INTEGER PRIMARY KEY,
    LbStationMesureEauxSurface   TEXT NOT NULL,
    CdPointEauxSurf              INTEGER,
    CdSupport                    INTEGER,
    LbSupport                    TEXT,
    DateDebutOperationPrelBio    DATE,
    CdListeFauFlor               TEXT,
    LbListeFauFlor               TEXT,
    CdTypListeFauFlor            TEXT,
    MnTypListeFauFlor            TEXT,
    CdTypTaxRep                  INTEGER,
    MnTypTaxRep                  TEXT,
    CdAppelTaxon                 INTEGER,
    NomLatinAppelTaxon           TEXT,
    RsTaxRep                     REAL,
    CdRqNbrTaxRep                INTEGER,
    MnemoRqNbrTaxRep             TEXT,
    CdUniteMesure                INTEGER,
    SymUniteMesure               TEXT,
    RefOperationPrelBio          TEXT,
    CdProducteur                 INTEGER,
    NomProducteur                TEXT
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