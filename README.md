# Proyecto Contaminación: 

Aplicación de visualización de los datos históricos de contaminantes de las principales estaciones de la ciudad de Madrid y desarrollo de un modelo de predicción de contaminantes e Índice de Contaminación del Aire basado en Prophet.

- /Desarrollo_Proyecto: notebooks y scripts desarrollados durante el transcurso del proyecto (scrapeo, procesamiento e inserción de los datos, modelos...)

- /lib : librería con df_preparation.py, llamada a BBDD, procesamiento de los datos y entrenamiento y predicción del modelo para la estación "Escuelas Aguirre".

- /static: archivo css, imágenes y svg estáticos de la app.

- /templates: plantillas html de las distintas vistas de la app.

- Dockerfile: construcción de la imagen de docker de la aplicación (docker build . -t miflask)

- docker-compose.yml: despliegue de los dos servicios de la aplicación, influxdb y app web (docker-compose up -d)

- app.py: código de la aplicación

### Home 

![image](https://user-images.githubusercontent.com/48119358/166470476-f8625af8-29a0-4d9c-a4eb-fa20141ee52e.png)

### Mapa interactivo / Histórico de las principales estaciones de Madrid 

![image](https://user-images.githubusercontent.com/48119358/166470754-73bb8168-8336-4f8b-aa9d-4ec4bc07819a.png)

### Visualizaciones del histórico y predicción (24 horas) de la estación "Escuelas Aguirre"

![image](https://user-images.githubusercontent.com/48119358/166470865-b519c42e-c6fc-4c4d-bc57-ef80341a46bd.png)

### Escala del Índice de Calidad del Aire y predicción del Índice (24 horas)

![image](https://user-images.githubusercontent.com/48119358/166471012-97a81928-6f2e-4fd5-b6cd-f7a1a4c7ed68.png)


