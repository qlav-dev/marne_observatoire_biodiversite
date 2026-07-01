# Install into the SAME Python you run (most reliable)

import pandas as pd


Res_ammonium = pd.read_csv('Naiades_filter\Analyses_Ammonium.CSV', sep=";", on_bad_lines="skip", dtype=str)
Res_temp = pd.read_csv('Naiades_filter\Analyses_Temp.CSV', sep=";", on_bad_lines="skip", dtype=str)
Res_DBO = pd.read_csv('Naiades_filter\Analyses_DBO5.CSV', sep=";", on_bad_lines="skip", dtype=str)

#print(Res_ammonium)
#print (Res_temp)
#print(Res_DBO) 


#print(Res_ammonium[['CdStationMesureEauxSurface','LbStationMesureEauxSurface','CdSupport','LbSupport','CdFractionAnalysee','LbFractionAnalysee','CdPrelevement','DatePrel','HeurePrel','DateAna','HeureAna','CdParametre','LbLongParamètre','RsAna','CdUniteMesure','SymUniteMesure'
#]])

ammonium_tri=Res_ammonium[['CdStationMesureEauxSurface','LbStationMesureEauxSurface','CdSupport','LbSupport','CdFractionAnalysee','LbFractionAnalysee','CdPrelevement','DatePrel','HeurePrel','DateAna','HeureAna','CdParametre','LbLongParamètre','RsAna','CdUniteMesure','SymUniteMesure'
]]

temp_tri=Res_temp[['CdStationMesureEauxSurface','LbStationMesureEauxSurface','CdSupport','LbSupport','CdFractionAnalysee','LbFractionAnalysee','CdPrelevement','DatePrel','HeurePrel','DateAna','HeureAna','CdParametre','LbLongParamètre','RsAna','CdUniteMesure','SymUniteMesure'
]]

dbo_tri=Res_DBO[['CdStationMesureEauxSurface','LbStationMesureEauxSurface','CdSupport','LbSupport','CdFractionAnalysee','LbFractionAnalysee','CdPrelevement','DatePrel','HeurePrel','DateAna','HeureAna','CdParametre','LbLongParamètre','RsAna','CdUniteMesure','SymUniteMesure'
]]

ammonium_tri.to_csv('ammonium.csv')
temp_tri.to_csv('temp.csv')
dbo_tri.to_csv('dbo5.csv')



