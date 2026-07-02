-- Table Stations avec tous les alias
DROP TABLE IF EXISTS Stations;

CREATE TABLE IF NOT EXISTS Stations (
    CdStationMesureEauxSurface INT PRIMARY KEY,
    LbStationMesureEauxSurface TEXT,
    DurStationMesureEauxSurface TEXT,
    CoordXStationMesureEauxSurface REAL,
    CoordYStationMesureEauxSurface REAL,
    CdProjStationMesureEauxSurface TEXT,
    LibelleProjection TEXT,
    CodeCommune TEXT,
    LbCommune TEXT,
    CodeDepartement TEXT, 
    LbDepartement TEXT,
    CodeRegion TEXT,
    LbRegion TEXT,
    CdMasseDEau TEXT,
    CdEuMasseDEau TEXT,
    NomMasseDEau TEXT,
    CdEuSsBassinDCEAdmin TEXT,    
    NomSsBassinDCEAdmin TEXT,
    CdBassinDCE TEXT,
    CdEuBassinDCE TEXT,
    NomEuBassinDCE TEXT,
    CdTronconHydrographique TEXT,
    CdCoursdEau TEXT,
    NomCoursdEau TEXT,
    CodeTypEthStationMesureEauxSurface TEXT,
    LibelleTypEthStationMesureEauxSurface TEXT,
    ComStationMesureEauxSurface TEXT,
    DateCreationStationMesureEauxSurface TEXT,    
    DateArretActiviteStationMesureEauxSurface TEXT,   
    DateMAJInfosStationMesureEauxSurface TEXT,
    FinaliteStationMesureEauxSurface TEXT,
    LocPreciseStationMesureEauxSurface TEXT,
    CodeNatureStationMesureEauxSurface TEXT,
    LibelleNatureStationMesureEauxSurface TEXT,
    AltitudePointCaracteritisque TEXT,
    PkPointTronconEntiteHydroPrincipale TEXT, 
    PremierMoisAnneeEtiage TEXT, 
    SuperficieBassinVersantReel TEXT, 
    SuperficieBassinVersantTopo TEXT
);

DROP TABLE IF EXISTS CEP;

CREATE TABLE IF NOT EXISTS CEP (
    CdStationMesureEauxSurface INTEGER,
    LbStationMesureEauxSurface TEXT,
    CdPointEauxSurf TEXT,
    CdSupport INTEGER,
    LbSupport TEXT,
    DateDebutOperationPrelBio TEXT,
    CdParametreEnv INTEGER,
    LbLongParametre TEXT,
    RsParEnvOpPrelBio REAL,
    CdUniteMesure INTEGER,
    SymUniteMesure TEXT,
    CdRqParEnvPrelBio INTEGER,
    MnemoRqParEnvPrelBio TEXT,
    CdMethodeParEnvPrelBio INTEGER,
    NomMethodeParEnvPrelBio TEXT,
    RefOperationPrelBio TEXT,
    CdStatutParEnvPrelBio INTEGER,
    MnStatutParEnvPrelBio TEXT,
    CdQualParEnvPrelBio INTEGER,
    LbQualParEnvPrelBio TEXT,
    DateParEnvPrelBio TEXT,
    CdProducteur TEXT,
    NomProducteur TEXT
);

-- Vue pour CEP avec alias
CREATE VIEW IF NOT EXISTS v_CEP AS
SELECT 
    CdStationMesureEauxSurface AS StationId,
    LbStationMesureEauxSurface AS StationName,
    CdPointEauxSurf AS WaterPointId,
    CdSupport AS SupportId,
    LbSupport AS SupportLabel,
    DateDebutOperationPrelBio AS OperationStartDate,
    CdParametreEnv AS ParameterId,
    LbLongParametre AS ParameterName,
    RsParEnvOpPrelBio AS ParameterValue,
    CdUniteMesure AS UnitId,
    SymUniteMesure AS UnitSymbol,
    CdRqParEnvPrelBio AS QualityRemarkId,
    MnemoRqParEnvPrelBio AS QualityRemarkCode,
    CdMethodeParEnvPrelBio AS MethodId,
    NomMethodeParEnvPrelBio AS MethodName,
    RefOperationPrelBio AS OperationReference,
    CdStatutParEnvPrelBio AS StatusId,
    MnStatutParEnvPrelBio AS StatusCode,
    CdQualParEnvPrelBio AS QualityId,
    LbQualParEnvPrelBio AS QualityLabel,
    DateParEnvPrelBio AS ParameterDate,
    CdProducteur AS ProducerId,
    NomProducteur AS ProducerName
FROM CEP;

DROP TABLE IF EXISTS FauneFlore;

CREATE TABLE IF NOT EXISTS FauneFlore (
    CdStationMesureEauxSurface INTEGER,
    LbStationMesureEauxSurface TEXT,
    CdPointEauxSurf TEXT,
    CdSupport INTEGER,
    LbSupport TEXT,
    DateDebutOperationPrelBio TEXT,
    CdListeFauFlor TEXT,
    LbListeFauFlor TEXT,
    CdTypListeFauFlor INTEGER,
    MnTypListeFauFlor TEXT,
    CdTypTaxRep INTEGER,
    MnTypTaxRep TEXT,
    CdAppelTaxon INTEGER,
    NomLatinAppelTaxon TEXT,
    RsTaxRep REAL,
    CdRqNbrTaxRep INTEGER,
    MnemoRqNbrTaxRep TEXT,
    CdUniteMesure INTEGER,
    SymUniteMesure TEXT,
    RefOperationPrelBio TEXT,
    CdProducteur TEXT,
    NomProducteur TEXT
);

-- Vue pour FauneFlore avec alias
CREATE VIEW IF NOT EXISTS v_FauneFlore AS
SELECT 
    CdStationMesureEauxSurface AS StationId,
    LbStationMesureEauxSurface AS StationName,
    CdPointEauxSurf AS WaterPointId,
    CdSupport AS SupportId,
    LbSupport AS SupportLabel,
    DateDebutOperationPrelBio AS OperationStartDate,
    CdListeFauFlor AS SpeciesListId,
    LbListeFauFlor AS SpeciesListName,
    CdTypListeFauFlor AS ListTypeId,
    MnTypListeFauFlor AS ListTypeCode,
    CdTypTaxRep AS TaxonRepTypeId,
    MnTypTaxRep AS TaxonRepTypeCode,
    CdAppelTaxon AS TaxonId,
    NomLatinAppelTaxon AS TaxonLatinName,
    RsTaxRep AS TaxonRepValue,
    CdRqNbrTaxRep AS QuantityRemarkId,
    MnemoRqNbrTaxRep AS QuantityRemarkCode,
    CdUniteMesure AS UnitId,
    SymUniteMesure AS UnitSymbol,
    RefOperationPrelBio AS OperationReference,
    CdProducteur AS ProducerId,
    NomProducteur AS ProducerName
FROM FauneFlore;

DROP TABLE IF EXISTS Operations;

CREATE TABLE IF NOT EXISTS Operations (
    CdStationMesureEauxSurface INTEGER,
    LbStationMesureEauxSurface TEXT,
    CdPointEauxSurf TEXT,
    CdSupport INTEGER,
    LbSupport TEXT,
    CdMethode INTEGER,
    NomLongMethodePrel TEXT,
    DateDebutOperationPrelBio TEXT,
    HeureDebutOperationPrelBio TEXT,
    DateFinOperationPrelbio TEXT,
    HeureFinOperationPrelBio TEXT,
    CdProducteur TEXT,
    NomProducteur TEXT,
    CdPreleveur TEXT,
    NomPreleveur TEXT,
    CdDeterminateur TEXT,
    NomDéterminateur TEXT,
    CodeSandreRdd TEXT,
    NomRdd TEXT,
    CdStatutResBioOperationPrelBio INTEGER,
    MnemoStatutResBioOperationPrelBio TEXT,
    CdQualResBioOperationPrelBio INTEGER,
    LbQualResBioOperationPrelBio TEXT,
    RefOperationPrelBio TEXT,
    ObjOperationPrelBio TEXT,
    LongProspecOperationPrelBio REAL,
    LargeurMoyLameEauOperationPrelBio REAL,
    HMoyLamOperationPrelBio REAL,
    SurfTotProspecteeOperationPrelBio REAL
);

-- Vue pour Operations avec alias
CREATE VIEW IF NOT EXISTS v_Operations AS
SELECT 
    CdStationMesureEauxSurface AS StationId,
    LbStationMesureEauxSurface AS StationName,
    CdPointEauxSurf AS WaterPointId,
    CdSupport AS SupportId,
    LbSupport AS SupportLabel,
    CdMethode AS MethodId,
    NomLongMethodePrel AS MethodLongName,
    DateDebutOperationPrelBio AS OperationStartDate,
    HeureDebutOperationPrelBio AS OperationStartTime,
    DateFinOperationPrelbio AS OperationEndDate,
    HeureFinOperationPrelBio AS OperationEndTime,
    CdProducteur AS ProducerId,
    NomProducteur AS ProducerName,
    CdPreleveur AS SamplerId,
    NomPreleveur AS SamplerName,
    CdDeterminateur AS DeterminerId,
    NomDéterminateur AS DeterminerName,
    CodeSandreRdd AS SandreCode,
    NomRdd AS RddName,
    CdStatutResBioOperationPrelBio AS StatusId,
    MnemoStatutResBioOperationPrelBio AS StatusCode,
    CdQualResBioOperationPrelBio AS QualityId,
    LbQualResBioOperationPrelBio AS QualityLabel,
    RefOperationPrelBio AS OperationReference,
    ObjOperationPrelBio AS OperationObjective,
    LongProspecOperationPrelBio AS ProspectionLength,
    LargeurMoyLameEauOperationPrelBio AS AverageWaterWidth,
    HMoyLamOperationPrelBio AS AverageWaterDepth,
    SurfTotProspecteeOperationPrelBio AS TotalProspectedArea
FROM Operations;

DROP TABLE IF EXISTS Resultats;

CREATE TABLE IF NOT EXISTS Resultats (
    CdStationMesureEauxSurface INTEGER,
    LbStationMesureEauxSurface TEXT,
    CdPointEauxSurf TEXT,
    DateDebutOperationPrelBio TEXT,
    CdSupport TEXT,
    LbSupport TEXT,
    DtProdResultatBiologique TEXT,
    HeureResultat TEXT,
    CdParametreResultatBiologique TEXT,
    LbLongParametre TEXT,
    ResIndiceResultatBiologique REAL,
    CdUniteMesure INTEGER,
    SymUniteMesure TEXT,
    CdRqIndiceResultatBiologique TEXT,
    MnemoRqAna TEXT,
    CdMethEval TEXT,
    RefOperationPrelBio TEXT,
    CdProducteur TEXT,
    NomProducteur TEXT,
    CdAccredRsIndiceResultatBiologique TEXT,
    MnAccredRsIndiceResultatBiologique TEXT
);

-- Vue pour Resultats avec alias
CREATE VIEW IF NOT EXISTS v_Resultats AS
SELECT 
    CdStationMesureEauxSurface AS StationId,
    LbStationMesureEauxSurface AS StationName,
    CdPointEauxSurf AS WaterPointId,
    DateDebutOperationPrelBio AS OperationStartDate,
    CdSupport AS SupportId,
    LbSupport AS SupportLabel,
    DtProdResultatBiologique AS ResultProductionDate,
    HeureResultat AS ResultTime,
    CdParametreResultatBiologique AS ParameterId,
    LbLongParametre AS ParameterName,
    ResIndiceResultatBiologique AS IndexResult,
    CdUniteMesure AS UnitId,
    SymUniteMesure AS UnitSymbol,
    CdRqIndiceResultatBiologique AS QualityRemarkId,
    MnemoRqAna AS QualityRemarkCode,
    CdMethEval AS EvaluationMethodId,
    RefOperationPrelBio AS OperationReference,
    CdProducteur AS ProducerId,
    NomProducteur AS ProducerName,
    CdAccredRsIndiceResultatBiologique AS AccreditationId,
    MnAccredRsIndiceResultatBiologique AS AccreditationCode
FROM Resultats;


CREATE TABLE IF NOT EXISTS Ammonium (
    CdStationMesureEauxSurface INTEGER
    LbStationMesureEauxSurface TEXT
    CdSupport INTEGER
    LbSupport TEXT
    CdFractionAnalysee INTEGER
    LbFractionAnalysee TEXT
    CdPrelevement INTEGER
    DatePrel DATE 
    HeurePre HOUR
    DateAna DATE 
    HeureAna HOUR
    CdParametre INTEGER
    LbLongParamètre TEXT
    RsAna REAL 
    CdUniteMesure INTEGER
    SymUniteMesure TEXT
);

CREATE TABLE IF NOT EXISTS Temperature (
    CdStationMesureEauxSurface INTEGER
    LbStationMesureEauxSurface TEXT
    CdSupport INTEGER
    LbSupport TEXT
    CdFractionAnalysee INTEGER
    LbFractionAnalysee TEXT
    CdPrelevement INTEGER
    DatePrel DATE 
    HeurePre HOUR
    DateAna DATE 
    HeureAna HOUR
    CdParametre INTEGER
    LbLongParamètre TEXT
    RsAna REAL 
    CdUniteMesure INTEGER
    SymUniteMesure TEXT
);

CREATE TABLE IF NOT EXISTS DBO5 (
    CdStationMesureEauxSurface INTEGER
    LbStationMesureEauxSurface TEXT
    CdSupport INTEGER
    LbSupport TEXT
    CdFractionAnalysee INTEGER
    LbFractionAnalysee TEXT
    CdPrelevement INTEGER
    DatePrel DATE 
    HeurePre HOUR
    DateAna DATE 
    HeureAna HOUR
    CdParametre INTEGER
    LbLongParamètre TEXT
    RsAna REAL 
    CdUniteMesure INTEGER
    SymUniteMesure TEXT
);

CREATE TABLE IF NOT EXISTS AnimauxProteges (
    CdStationMesureEauxSurfac,
    LbStationMesureEauxSurfac,
    CdPointEauxSu,
    CdSupport,
    LbSupport,
    DateDebutOperationPrelBio,
    CdListeFauFlo,
    LbListeFauFlo,
    CdTypListeFauFlor,
    MnTypListeFauFlor,
    CdTypTaxR,
    MnTypTaxR,
    CdAppelTaxon ,
    NomLatinAppelTaxo,
    RsTaxRep ,
    CdRqNbrTaxRep,
    MnemoRqNbrTaxRep ,
    CdUniteMesure,
    SymUniteMesur,
    RefOperationPrelB,
    CdProducteur ,
    NomProducteur,
    CD_NO,
    CD_RE,
    CD_SU,
    CD_TYPE_STATU,
    LB_TYPE_STATU,
    REGROUPEMENT_TYPE,
    CODE_STAT,
    LABEL_STATUT ,
    CD_SI,
    LB_AUTEUR,
    REGNE,
    PHYLU,
    CLASS,
    ORDRE,
    FAMIL,
    GROUP1_IN,
    GROUP2_IN,);

