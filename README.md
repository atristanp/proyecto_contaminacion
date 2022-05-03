# Proyecto Contaminación: 

Aplicación de visualización de los datos históricos de contaminantes de las principales estaciones de la ciudad de Madrid y desarrollo de un modelo de predicción de contaminantes e Índice de Contaminación del Aire basado en Prophet.


- /lib : librería con df_preparation.py, llamada a BBDD, procesamiento de los datos y entrenamiento y predicción del modelo para la estación "Escuelas Aguirre".
- /static: archivo css, imágenes y svg estáticos de la app.
- /templates: plantillas html de las distintas vistas de la app.
- Dockerfile: construcción de la imagen de docker de la aplicación (docker build . -t miflask)
- docker-compose.yml: despliegue de los dos servicios de la aplicación, influxdb y app web (docker-compose up -d)
- app.py: código de la aplicación
