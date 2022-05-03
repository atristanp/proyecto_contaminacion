from flask import Flask, render_template, request, Markup  #
# from influxdb import DataFrameClient

import folium
from folium.plugins import MiniMap

import altair as alt
from altair import Chart, X, Y, Axis

# from folium.plugins import FastMarkerCluster
# from folium.plugins import Fullscreen
# from folium import FeatureGroup, LayerControl, Map, Marker
# import datetime

# import requests
import json
from datetime import datetime, timedelta

import pandas as pd

# import numpy as np

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True  # Para poder recargar la template del mapa en cada llamada

import lib.df_preparation as df_prep

df_preparation = df_prep.df_preparation()

initial_data = pd.DataFrame({
    'lat': [40.421599, 40.420216, 40.439918, 40.398163, 40.465640, 40.439616, 40.423366, 40.451514, 40.394789,
            40.450660],
    'lon': [-3.681781, -3.749114, -3.639458, -3.686695, -3.688991, -3.690691, -3.712288, -3.676831, -3.731890,
            -3.710696],
    'name': ['Escuelas Aguirre', 'Casa de Campo', 'Arturo Soria', 'Méndez Álvaro', 'Plaza de Castilla',
             'Castellana', 'Plaza de España', 'Ramón y Cajal', 'Farolillo', 'Cuatro Caminos'],
    'estacion': ['ESTACION_8', 'ESTACION_24', 'ESTACION_16', 'ESTACION_47', 'ESTACION_50', 'ESTACION_48', 'ESTACION_4',
                 'ESTACION_11', 'ESTACION_18', 'ESTACION_38'],
    'SO2': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'NO2': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'PM10': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'PM2.5': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'O3': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'ICA': ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
    'Categoria': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],

})  # , dtype=str


def color_producer(value):
    if value == 0:
        return "green"
    elif value == 1:
        return "lightgreen"

    elif value == 2:
        return "orange"

    elif value == 3:
        return "red"
    elif value == 4:
        return "darkred"

    elif value == -1:
        return "gray"


domain = ['0', '1', '2', '3', '4']
range_ = ['green', 'lightgreen', 'orange', 'red', 'darkred']

"""

# Indice calidad del aire
# Método 1:
def getICAPM25(cont):
    if 0 <= cont <= 10:
        return cont, 0
    elif 11 <= cont <= 20:
        return cont, 1
    elif 21 <= cont <= 25:
        return cont, 2
    elif 26 <= cont <= 50:
        return cont, 3
    elif cont > 50:
        return cont, 4
    else:
        return 0, -1


def getICAPM10(cont):
    if 0 <= cont <= 20:
        return cont, 0
    elif 21 <= cont <= 35:
        return cont, 1
    elif 36 <= cont <= 50:
        return cont, 2
    elif 51 <= cont <= 100:
        return cont, 3
    elif cont > 100:
        return cont, 4
    else:
        return 0, -1


def getICANO2(cont):
    if 0 <= cont <= 40:
        return cont, 0
    elif 41 <= cont <= 100:
        return cont, 1
    elif 101 <= cont <= 200:
        return cont, 2
    elif 201 <= cont <= 400:
        return cont, 3
    elif cont > 400:
        return cont, 4
    else:
        return 0, -1


def getICAO3(cont):
    if 0 <= cont <= 80:
        return cont, 0
    elif 81 <= cont <= 120:
        return cont, 1
    elif 121 <= cont <= 180:
        return cont, 2
    elif 181 <= cont <= 240:
        return cont, 3
    elif cont > 241:
        return cont, 4
    else:
        return 0, -1


def getICASO2(cont):
    if 0 <= cont <= 100:
        return cont, 0
    elif 101 <= cont <= 200:
        return cont, 1
    elif 201 <= cont <= 350:
        return cont, 2
    elif 351 <= cont <= 500:
        return cont, 3
    elif cont > 501:
        return cont, 4
    else:
        return 0, -1


def getPeorICA(PM25, PM10, NO2, O3, SO2):
    datosICA = [getICAPM25(PM25), getICAPM10(PM10), getICANO2(NO2), getICAO3(O3), getICASO2(SO2)]
    datosICA = sorted(datosICA, key=lambda tup: tup[1], reverse=True)
    return sorted(datosICA, key=lambda tup: tup[0], reverse=True)[0]


def calculaICA(datos):
    # print(datos)
    datos['ICA'] = datos.apply(lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[0],
                               axis=1)
    datos['Categoria'] = datos.apply(
        lambda row: getPeorICA(row['PM25'], row['PM10'], row['NO2'], row['O3'], row['SO2'])[1], axis=1)
    return datos

"""


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    # df_preparation.df_list['ESTACION_8'].copy() -> copia del df entero sobre el que modificar

    my_prediccion = json.loads(df_preparation.df_prediccion.to_json(orient="table"))

    alt.data_transformers.disable_max_rows()
    n = 4380
    s = "últimos 6 meses"
    title1 = "ICA" + s
    if request.method == "POST":
        n = int(request.form.get("pred").split()[0]) * 744
        if int(request.form.get("pred").split()[0]) == 1:
            s = "últimos 30 días"
        else:
            s = "últimos " + request.form.get("pred")

    title1 = "ICA " + s

    chart1_data = df_preparation.df_list['ESTACION_8'].copy().reset_index(level=0).tail(n)
    chart1_data = chart1_data[chart1_data.Categoria != -1]

    interval = alt.selection_interval(encodings=['x'])

    base = Chart(chart1_data).mark_point(color='gray').encode(
        X('index', axis=Axis(title=title1)),
        Y('Categoria', axis=Axis(title='', values=list(range(0, 5))), scale=alt.Scale(domain=[0, 4], clamp=True)),
        color=alt.Color('Categoria', scale=alt.Scale(domain=domain, range=range_),
                        legend=alt.Legend(title="ICA")),
        tooltip=['index', 'Categoria'])
    hist = Chart(chart1_data).mark_bar().encode(
        x=alt.X('count()', axis=alt.Axis(title='')),
        y=alt.X('Categoria', axis=alt.Axis(title='', values=list(range(0, 5)))),
        color=alt.Color('Categoria', scale=alt.Scale(domain=domain, range=range_))).properties(
        height=80).transform_filter(interval)
    upper = base.interactive()
    lower = base.encode(X('index', axis=Axis(title='')),
                        Y('Categoria', axis=Axis(title=''), scale=alt.Scale(domain=[0, 4], clamp=True))).properties(
        height=80).add_selection(interval)
    chart_html = alt.vconcat(alt.vconcat(upper, lower), hist).configure(background='transparent').to_html()

    chart2_data = df_preparation.df_list['ESTACION_8'].copy().reset_index(level=0).tail(168)
    datosPre = json.loads(chart2_data.to_json(orient="table"))

    labels = []
    for i in range(24):
        labels.append((datetime.today() + timedelta(hours=i + 1)).strftime("%y/%m/%d %H:%M")[:-2] + "00")

    return render_template('prediction.html', chart_html=Markup(chart_html), s=s, datosPre=datosPre,
                           my_prediccion=my_prediccion, labels=labels)


"""
@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    # df_preparation.df_list['ESTACION_8'].copy() -> copia del df entero sobre el que modificar
    alt.data_transformers.disable_max_rows()
    n = 4380
    s = "últimos 6 meses"
    title1 = "ICA" + s
    if request.method == "POST":
        n = int(request.form.get("pred").split()[0]) * 744
        if int(request.form.get("pred").split()[0]) == 1:
            s = "últimos 30 días"
        else:
            s = "últimos " + request.form.get("pred")

    title1 = "ICA " + s

    chart1_data = df_preparation.df_list['ESTACION_8'].copy().reset_index(level=0).tail(n)
    chart1_data = chart1_data[chart1_data.Categoria != -1]
    print(chart1_data)

    interval = alt.selection_interval(encodings=['x'])

    base = Chart(chart1_data).mark_point(color='gray').encode(
        X('index', axis=Axis(title=title1)),
        Y('Categoria', axis=Axis(title='', values=list(range(0, 5))), scale=alt.Scale(domain=[0, 4], clamp=True)),
        color=alt.Color('Categoria', scale=alt.Scale(domain=domain, range=range_),
                        legend=alt.Legend(title="Nivel de contaminación")),
        tooltip=['index', 'Categoria'])
    hist = Chart(chart1_data).mark_bar().encode(
        x=alt.X('count()', axis=alt.Axis(title='')),
        y=alt.X('Categoria', axis=alt.Axis(title='', values=list(range(0, 5)))),
        color=alt.Color('Categoria', scale=alt.Scale(domain=domain, range=range_))).properties(
        height=80).transform_filter(interval)
    upper = base.interactive()
    lower = base.encode(X('index', axis=Axis(title='')),
                        Y('Categoria', axis=Axis(title=''), scale=alt.Scale(domain=[0, 4], clamp=True))).properties(
        height=80).add_selection(interval)
    chart_html = alt.vconcat(alt.vconcat(upper, lower), hist).configure(background='transparent').to_html()

    chart2_data = df_preparation.df_list['ESTACION_8'].copy().reset_index(level=0).tail(168)
    datosPre = json.loads(chart2_data.to_json(orient="table"))


    print(df_preparation.df_prediccion)

    return render_template('prediction.html', chart_html=Markup(chart_html), s=s, datosPre=datosPre)

"""


@app.route('/map', methods=['GET'])
def well_map():
    data = initial_data.copy()

    print(request)

    print(data)

    print('EXAMPLE: 2022-02-28 23:00:00+00:00')

    date_query = request.args.get('date_form')

    print(date_query)

    print(df_preparation.df_list['ESTACION_8'].iloc[-1:].index)
    date_max = df_preparation.df_list['ESTACION_8'].iloc[-1:].index.strftime("%Y-%m-%dT%H:%M").values

    if date_query is None:
        date_actual = date_max[0]

    else:
        date_actual = date_query

    for i in df_preparation.estaciones:

        if date_query is None:

            estacion_row = df_preparation.df_list[f'{i}'].loc[
                df_preparation.df_list[f'{i}'].index == date_max[0]]  # Máxima fecha posible = más reciente

        else:
            date_query = date_query.replace("T", " ")

            estacion_row = df_preparation.df_list[f'{i}'].loc[
                df_preparation.df_list[f'{i}'].index == date_query]

            # print(data.loc[data["name"] == "Escuelas Aguirre", "SO2"])
        try:
            data.loc[data["estacion"] == f'{i}', "SO2"] = float(estacion_row["SO2"])
        except:
            pass

        try:
            data.loc[data["estacion"] == f'{i}', "NO2"] = float(estacion_row["NO2"])
        except:
            pass
        try:
            data.loc[data["estacion"] == f'{i}', "PM10"] = float(estacion_row["PM10"])
        except:
            pass

        try:
            data.loc[data["estacion"] == f'{i}', "PM2.5"] = float(estacion_row["PM25"])
        except:
            pass

        try:
            data.loc[data["estacion"] == f'{i}', "O3"] = float(estacion_row["O3"])
        except:
            pass

        print(estacion_row)
        print(estacion_row["ICA"])
        print(type(estacion_row["ICA"]))
        print(estacion_row["Categoria"])
        print(type(estacion_row["Categoria"]))

        try:
            data.loc[data["estacion"] == f'{i}', "ICA"] = float(estacion_row["ICA"])
        except:
            pass

        try:
            data.loc[data["estacion"] == f'{i}', "Categoria"] = int(estacion_row["Categoria"])
        except:
            pass

    print(data)

    m = folium.Map(location=[initial_data["lat"].mean(), initial_data["lon"].mean()],
                   tiles="cartodbpositron",
                   # width=1530, height=630,
                   # width="%100",
                   # height="%100",
                   zoom_start=12,
                   min_zoom=12)

    m.add_child(MiniMap())

    for i in range(0, len(data)):
        color = color_producer(int(data.iloc[i]['Categoria']))
        print(color)

        html = f"""
                        <h3> ICA {data.iloc[i]['name']}: <span style="color:{color};">{data.iloc[i]['ICA']}</span></h3>


                        <table class="table">
                          <thead>
                            
                            <!--<tr>
                              <th scope="col">ICA: </th>
                              <th scope="col">{data.iloc[i]['ICA']} (µg/m³)</th>
                            </tr> -->
                            
                            <tr>
                              <th scope="col">Contaminante</th>
                              <th scope="col">Concentración (µg/m³)</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td align="center">NO2</td>
                              <td align="center"><b>{data.iloc[i]['NO2']}</b></td>
                            </tr>
                            <tr>
                              <td align="center">O3</td>
                              <td align="center"><b>{data.iloc[i]['O3']}</b></td>
                            </tr>
                            <tr>
                              <td align="center">PM2.5</td>
                              <td align="center"><b>{data.iloc[i]['PM2.5']}</b></td>
                            </tr>
                            <tr>
                              <td align="center">PM10</td>
                              <td align="center"><b>{data.iloc[i]['PM10']}</b></td>
                            </tr>
                            <tr>
                              <td align="center">SO2</td>
                              <td align="center"><b>{data.iloc[i]['SO2']}</b></td>
                            </tr>
                          </tbody>
                        </table>

                        """

        iframe = folium.IFrame(html=html, width=300, height=300)
        popup = folium.Popup(iframe, max_width=2650)

        folium.Marker(
            location=(data.iloc[i]['lat'], data.iloc[i]['lon']),
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(m)

        folium.Circle(
            location=(data.iloc[i]['lat'], data.iloc[i]['lon']),
            color=color,
            fill_color=color,
            tooltip=data.iloc[i]['name'],
            radius=40,

            weight=4,
            fill_opacity=0.5,

        ).add_to(m)

    m.save("templates/map_created.html")

    return render_template('map.html', date_max=date_max[0], date_actual=date_actual)  # 2001-01-01T00:00


from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", debug=True, port=5000) # Debug server
