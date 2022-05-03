from influxdb import DataFrameClient
from prophet import Prophet
from prophet.serialize import model_from_json

import pandas as pd
import json


# Indice calidad del aire
# Método 1:
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
    return datosICA[0]


def calculaICA(datos):
    datos['ICA'] = datos.apply(lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[0],
                               axis=1)
    datos['Categoria'] = datos.apply(
        lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[1], axis=1)
    return datos


def getDatosFuturo(model, period):
    return model.predict(model.make_future_dataframe(periods=period, freq='60min'))


def loadModel(nombre):
    nombre = nombre + ".json"
    print(nombre)
    with open(nombre, 'r') as fin:
        return model_from_json(json.load(fin))  # Load model


class df_preparation:
    """
        df_preparation:
    """

    def __init__(self):
        dbhost = '34.79.253.2'
        dbport = 8086
        dbuser = 'root'
        dbpasswd = '12345678'
        dbname = 'registros_contaminacion'

        self.client = DataFrameClient(dbhost, dbport, dbuser, dbpasswd, dbname)

        self.estaciones = ['ESTACION_8', 'ESTACION_24', 'ESTACION_16', 'ESTACION_47', 'ESTACION_50', 'ESTACION_48',
                           'ESTACION_4', 'ESTACION_11', 'ESTACION_18', 'ESTACION_38']
        self.df_list = {}

        self.load_dfs()

        self.df_prediccion = self.prediction()

        for i in self.estaciones:
            self.df_list[f'{i}'] = self.df_list[f'{i}'].fillna('--')

        print("AQUIIIIIIIIIIIII, ", self.df_list)

    def load_dfs(self):
        for i in self.estaciones:
            self.df_list[f'{i}'] = self.client.query(f'select * from {i}')[
                f'{i}']  # result es un dict, result['ESTACION8'] es un df

            # print(self.df_list[f'{i}'].columns)
            # self.df_list[f'{i}'] = validadf(self.df_list[f'{i}'])
            # self.df_list[f'{i}'] = calculaICA(self.df_list[f'{i}'])

            # print(self.df_list[f'{i}'].isnull().sum())

            # self.df_list[f'{i}'] = calculaICA(self.df_list[f'{i}'])

    def prediction(self):



        # Devuelve el dataframe
        def getDF(datos, Contaminante):
            prophet_df = datos[[Contaminante]].reset_index().rename(columns={'index': 'ds', Contaminante: 'y'})
            prophet_df['ds'] = prophet_df['ds'].dt.tz_localize(None)
            return prophet_df

        # self.df_list['ESTACION_8']

        def entrenar_modelo(datos):
            m = Prophet()
            m.fit(datos)
            return m

        PM25_train = getDF(self.df_list['ESTACION_8'], "PM25")
        m_PM25 = entrenar_modelo(PM25_train)

        PM10_train = getDF(self.df_list['ESTACION_8'], "PM10")
        m_PM10 = entrenar_modelo(PM10_train)

        NO2_train = getDF(self.df_list['ESTACION_8'], "NO2")
        m_NO2 = entrenar_modelo(NO2_train)

        O3_train = getDF(self.df_list['ESTACION_8'], "O3")
        m_O3 = entrenar_modelo(O3_train)

        SO2_train = getDF(self.df_list['ESTACION_8'], "SO2")
        m_S02 = entrenar_modelo(SO2_train)

        # m_PM25 = loadModel('m_PM25')
        # m_PM10 = loadModel('m_PM10')
        # m_NO2 = loadModel('m_NO2')
        # m_O3 = loadModel('m_O3')
        # m_S02 = loadModel('m_S02')

        p_PM25 = getDatosFuturo(m_PM25, 24)
        print("1")
        p_PM10 = getDatosFuturo(m_PM10, 24)
        print("2")
        p_NO2 = getDatosFuturo(m_NO2, 24)
        print("3")
        p_O3 = getDatosFuturo(m_O3, 24)
        print("4")
        p_SO2 = getDatosFuturo(m_S02, 24)

        print("5")

        data = [p_PM25[-24:]['ds'], p_PM25[-24:]['yhat'], p_PM10[-24:]['yhat'], p_NO2[-24:]['yhat'], p_O3[-24:]['yhat'],
                p_SO2[-24:]['yhat']]
        headers = ["fecha", "PM25", "PM10", "NO2", "O3", "SO2"]
        completed_prediction = pd.concat(data, axis=1, keys=headers)

        prediccion_final = calculaICA(completed_prediction)

        prediccion_final.to_csv('prediction.csv')


        """

        prediccion_final = pd.read_csv('prediction.csv')

        
        """

        print("PREDICCIÓN FINAL:\n", prediccion_final)

        return prediccion_final
