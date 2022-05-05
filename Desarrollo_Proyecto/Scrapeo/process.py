#!/usr/bin/env python3.7
import os
import numpy as np
import pandas as pd
import datetime
from influxdb import DataFrameClient, InfluxDBClient

def validadf(datos):
    if 'PM25' not in datos:
        datos["PM25"] = np.nan
    if 'PM10' not in datos:
        datos["PM10"] = np.nan
    if 'NO2' not in datos:
        datos["NO2"] = np.nan
    if 'O3' not in datos:
        datos["O3"] = np.nan
    if 'SO2' not in datos:
        datos["SO2"] = np.nan
    return datos

def getICAPM25(cont):
    if cont >= 0 and cont <= 10:
        return ((cont, 0))
    elif cont >= 11 and cont <= 20:
        return ((cont, 1))
    elif cont >= 21 and cont <= 25:
        return ((cont, 2))
    elif cont >= 26 and cont <= 50:
        return ((cont, 3))
    elif cont > 50:
        return ((cont, 4))
    else:
        return ((0, -1))

def getICAPM10(cont):
    if cont >= 0 and cont <= 20:
        return ((cont, 0))
    elif cont >= 21 and cont <= 35:
        return ((cont, 1))
    elif cont >= 36 and cont <= 50:
        return ((cont, 2))
    elif cont >= 51 and cont <= 100:
        return ((cont, 3))
    elif cont > 100:
        return ((cont, 4))
    else:
        return ((0, -1))

def getICANO2(cont):
    if cont >= 0 and cont <= 40:
        return ((cont, 0))
    elif cont >= 41 and cont <= 100:
        return ((cont, 1))
    elif cont >= 101 and cont <= 200:
        return ((cont, 2))
    elif cont >= 201 and cont <= 400:
        return ((cont, 3))
    elif cont > 400:
        return ((cont, 4))
    else:
        return ((0, -1))

def getICAO3(cont):
    if cont >= 0 and cont <= 80:
        return ((cont, 0))
    elif cont >= 81 and cont <= 120:
        return ((cont, 1))
    elif cont >= 121 and cont <= 180:
        return ((cont, 2))
    elif cont >= 181 and cont <= 240:
        return ((cont, 3))
    elif cont > 241:
        return ((cont, 4))
    else:
        return ((0, -1))

def getICASO2(cont):
    if cont >= 0 and cont <= 100:
        return ((cont, 0))
    elif cont >= 101 and cont <= 200:
        return ((cont, 1))
    elif cont >= 201 and cont <= 350:
        return ((cont, 2))
    elif cont >= 351 and cont <= 500:
        return ((cont, 3))
    elif cont > 501:
        return ((cont, 4))
    else:
        return ((0, -1))

def getPeorICA(PM25, PM10, NO2, O3, SO2):
    datosICA = [getICAPM25(PM25), getICAPM10(PM10), getICANO2(NO2), getICAO3(O3), getICASO2(SO2)]
    datosICA = sorted(datosICA, key=lambda tup: tup[1], reverse=True)
    return sorted(datosICA, key=lambda tup: tup[0], reverse=True)[0]

def calculaICA(datos):
    datos['ICA'] = datos.apply(lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[0],
                               axis=1)
    datos['Categoria'] = datos.apply(
        lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[1], axis=1)
    return datos

df = pd.read_csv("/home/proyectos_contaminacion/daily_data/download/horario.csv",sep=';')
df['HORAS'] = df.apply(lambda x: list([x['H01'], x['H02'], x['H03'],x['H04'],x['H05'],x['H06'],x['H07'],x['H08'],x['H09'],x['H10'],x['H11'],x['H12'],x['H13'],x['H14'],x['H15'],x['H16'],x['H17'],x['H18'],x['H19'],x['H20'],x['H21'],x['H22'],x['H23'],x['H24']]),axis=1)  
df['VALIDACIONES'] = df.apply(lambda x: list([x['V01'], x['V02'], x['V03'],x['V04'],x['V05'],x['V06'],x['V07'],x['V08'],x['V09'],x['V10'],x['V11'],x['V12'],x['V13'],x['V14'],x['V15'],x['V16'],x['V17'],x['V18'],x['V19'],x['V20'],x['V21'],x['V22'],x['V23'],x['V24']]),axis=1)
mapper = {
        1:"SO2",6:"CO",7:"NO",
        8:"NO2",9:"PM25",10:"PM10",
        12:"NOx",14:"O3",20:"TOL",
        30:"BEN",35:"EBE",37:"MXY",
        38:"PXY",39:"OXY",42:"TCH", 43:"CH4", 44:"NMHC"
    }
df_final = df.explode(['HORAS','VALIDACIONES'])
df_final = df_final.drop(df_final.columns[8:56], axis = 1) # drop de columnas (horas y validaciones)
df_final = df_final.drop(df_final.columns[0:2], axis = 1) # drop de columnas (provincia y municipio)
df_final = df_final.rename(columns={"HORAS": "VALOR", "VALIDACIONES": "VALIDO"}) # Rename de columnas
df_final['MAGNITUD'] = df_final['MAGNITUD'].map(mapper) # Mapping de filas
df_final = df_final.reset_index() # reset del índice ya que al generar 24 filas por cada registro hay duplicados
df_final = df_final.reset_index() # está 2 veces a propósito para generar una columna con todos los índices finales
df_final['HORA'] = df_final.apply(lambda x: x['level_0'] % 24, axis = 1) # Asignación de hora para cada registro
df_final = df_final.drop(['level_0'], axis = 1)
df_final = df_final.drop(['index'], axis = 1) # drop de las columnas index que se generan automáticamente al resetear el índice
df_final['FECHA'] = df_final.apply(lambda x: f"{x['ANO']}-{x['MES']}-{x['DIA']}-{x['HORA']}", axis = 1)
df_final['FECHA'] = df_final['FECHA'].apply(lambda col : datetime.datetime.strptime(col, '%Y-%m-%d-%H'))
df_final = df_final.drop(['ANO','MES','DIA','HORA'], axis = 1) # drop de columnas (ANO, MES, DIA, HORA)
df_final = df_final.astype({'MAGNITUD': 'string', 'PUNTO_MUESTREO': 'string', 'VALOR': 'int64', 'VALIDO':'string'}) # Casteo
df_final.set_index('FECHA', inplace = True) # Seteo del índice temporal para insertar en influxdb cloud
df_final = df_final.sort_values("FECHA")

dbhost = '34.79.253.2' #'34.88.128.173' # Cuidado! Google Cloud puede cambiar la ip pública!
dbport = 8086
dbuser = 'root'
dbpasswd = '12345678'
protocol = 'json'
dbname = 'registros_contaminacion'
df_client = DataFrameClient(dbhost, dbport, dbuser, dbpasswd, dbname)
for est in df_final['ESTACION'].unique():
    df_estacion = df_final[(df_final['ESTACION'] == est) & (df_final['VALIDO'] == 'V')].sort_values("FECHA")
    df_list = []
    for i in df_estacion['MAGNITUD'].unique(): # Valores únicos de la columna magnitud
        df_estacion[f'{i}'] = np.where(df_estacion['MAGNITUD'] == i,df_estacion['VALOR'],None)
        df_temp = df_estacion[df_estacion['MAGNITUD'] == i]
        df_list.append(df_temp)
    try:
        df_concatenado = pd.concat(df_list, axis=1).drop(columns=['VALOR','VALIDO','MAGNITUD','ESTACION']) #ignore_index=True
        df_concatenado = df_concatenado.loc[:,~df_concatenado.columns.duplicated()] # Elimina columnas duplicadas
        df_concatenado = validadf(df_concatenado)
        df_concatenado = calculaICA(df_concatenado)
        df_client.write_points(dataframe=df_concatenado, measurement=f'ESTACION_{est}', protocol='json') #json protocol, qué implica?
    except:
        pass

print(datetime.datetime.now(),end="\t")
print(df_client.get_list_database(),end="\t")
print(len(df_final))
