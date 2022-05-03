FROM continuumio/miniconda3

ADD . /code
WORKDIR /code

RUN conda install -c conda-forge pandas
RUN conda install -c conda-forge folium==0.12.1.post1
RUN conda install -c conda-forge flask
RUN conda install -c conda-forge altair==4.2.0
RUN conda install -c conda-forge waitress==2.1.1
RUN conda install -c conda-forge prophet==1.0.1
RUN conda install -c conda-forge influxdb==5.3.1

CMD python3 app.py
