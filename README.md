# P1_MLOPs_Steam_Games

Este es el repositorio del Proyecto Individual Nº1 Machine Learning Operations (MLOps).

## Datos


### Este proyecto utiliza tres archivos JSON:

- #### australian_user_reviews.json:
Contiene comentarios de usuarios sobre los juegos que consumen.
Datos adicionales incluyen si recomiendan el juego, emoticones de gracioso, y estadísticas sobre la utilidad del comentario.
También muestra el ID del usuario que comenta con su URL de perfil, y el ID del juego comentado.

- #### australian_users_items.json:
Contiene información sobre los juegos que juegan todos los usuarios.
Incluye el tiempo acumulado que cada usuario jugó a un juego específico.

- #### output_steam_games.json:
Contiene datos relacionados con los juegos en sí.
Incluye títulos, desarrolladores, precios, características técnicas, etiquetas y más.

Tanto el diccionario de datos como los datasets se encuentran en este [link](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj).
En el "Diccionario de datos" se detallan las variables de cada conjunto de datos.


## Transformaciones
Se llevó a cabo el proceso de extracción, transformación y carga (ETL) de tres conjuntos de datos proporcionados. Dos de estos conjuntos estaban estructurados de forma anidada, lo que
significa que contenían columnas con diccionarios o listas de diccionarios. Para abordar esto, se implementaron diversas estrategias para transformar las claves de estos diccionarios en
columnas separadas. Además, se realizó el relleno de valores nulos en variables fundamentales para el proyecto y se eliminaron columnas con una gran cantidad de valores nulos o que no
contribuían al objetivo del proyecto. Este proceso de optimización se llevó a cabo para mejorar el rendimiento de la API y se consideraron las limitaciones de almacenamiento en el
despliegue. Para realizar estas transformaciones, se empleó la librería Pandas.

## Feature Engineering
En este proyecto, se implementó un análisis de sentimiento para los reviews de usuarios de un juego. Se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna de
reviews originales, clasificando los sentimientos de los comentarios en una escala de 0 a 2:

0 para malo,
1 para neutral o sin review, y
2 para positivo.
Se utilizó la biblioteca TextBlob de procesamiento de lenguaje natural (NLP) en Python para llevar a cabo este análisis de sentimiento básico como parte de una prueba de concepto. El
objetivo fue asignar un valor numérico a los comentarios de los usuarios para representar si el sentimiento expresado era negativo, neutral o positivo.

El proceso consistió en tomar cada revisión de texto como entrada, usar TextBlob para calcular la polaridad de sentimiento y luego clasificar la revisión como negativa, neutral o
positiva basándose en la polaridad calculada. Para este análisis, se utilizaron los umbrales por defecto del modelo de TextBlob, donde las polaridades por debajo de -0.2 fueron
consideradas negativas, por encima de 0.2 positivas, y entre -0.2 y 0.2 como neutrales.

Además, con el objetivo de optimizar los tiempos de respuesta de las consultas en la API y considerando las limitaciones de almacenamiento en el servicio de nube para el deployment de
la API, se crearon dataframes auxiliares para cada una de las funciones solicitadas. Estos dataframes se guardaron en formato parquet, lo que permite una compresión y codificación
eficiente de los datos.

## Análisis exploratorio de los datos
Se realizó un Análisis Exploratorio de Datos (EDA) en tres conjuntos de datos tras el proceso de Extracción, Transformación y Carga (ETL), con el fin de identificar las variables
adecuadas para el modelo de recomendación. Para este análisis, se empleó la librería Pandas para la manipulación de datos, y Matplotlib junto a Seaborn para la visualización.

Específicamente para el modelo de recomendación, se optó por construir un dataframe especial que incluye el ID del usuario que realizó las reseñas, los nombres de los juegos comentados,
y una columna de rating generada a partir de un análisis de sentimientos combinado con recomendaciones de juegos.


## Modelo de aprendizaje automático
Se desarrollaron dos modelos de recomendación para juegos:

- Modelo Ítem-Ítem:
Este modelo se basa en la relación ítem-ítem. Al ingresar el nombre de un juego, el sistema genera una lista de 5 juegos similares. Esto se logra evaluando qué tan parecido es el juego
ingresado con el resto de los juegos en la base de datos y recomendando los más similares.

- Modelo Usuario-Juego:
En este caso, el modelo se enfoca en el filtro usuario-juego. Al ingresar el ID de un usuario, el sistema encuentra usuarios similares a él y recomienda juegos que a esos usuarios les
gustaron. Luego, recomienda esos juegos al usuario en cuestión.
Ambos modelos se basan en algoritmos de memoria, los cuales abordan el problema del filtrado colaborativo utilizando toda la base de datos. Se busca encontrar usuarios con preferencias
similares al usuario activo (el que recibe las recomendaciones) y utilizar esas preferencias para predecir qué juegos le podrían gustar.

Para medir la similitud entre juegos (item_similarity) y entre usuarios (user_similarity), se utilizó la similitud del coseno. Esta medida es comúnmente empleada en sistemas de
recomendación y análisis de datos. El coseno del ángulo entre los vectores que representan los juegos o usuarios se usa para determinar cuán similares son, evaluando la similitud en un
espacio multidimensional.

## Desarollo api
Se desarrolló una API utilizando el framework FastAPI, que incluye las siguientes funciones:

- userdata: Recibe el parámetro 'user_id' y devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad total de reviews
analizadas, y la cantidad de items que consume el usuario.

- countreviews: Se ingresan dos fechas para hacer una consulta y devuelve la cantidad de usuarios que realizaron reviews entre esas fechas, junto con el porcentaje de recomendaciones
positivas (True) que hicieron.

- genre: Recibe un género de videojuego como parámetro y devuelve el puesto en el que se encuentra ese género en un ranking, basado en la cantidad de horas jugadas para cada género.

- userforgenre: Recibe el género de un videojuego y devuelve el top 5 de usuarios con más horas de juego en ese género, indicando el id del usuario y el URL de su perfil.

- developer: Recibe el parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla esa empresa, junto con el porcentaje de
contenido Free por año sobre el total que desarrolla.

- sentiment_analysis: Recibe el año de lanzamiento de un juego y devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados con análisis de sentimiento, como
Negativo, Neutral y Positivo.

- recomendacion_juego: Recibe el nombre de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.

- recomendacion_usuario: Recibe el id de un usuario y devuelve una lista con 5 juegos recomendados para ese usuario, teniendo en cuenta las similitudes entre los usuarios.

Es importante destacar que, aunque ambas funciones de recomendación (recomendacion_juego y recomendacion_usuario) fueron agregadas a la API, solo recomendacion_juego pudo ser
desplegada en Render debido a que el conjunto de datos necesario para la predicción excedía la capacidad de almacenamiento disponible. Por lo tanto, para utilizar recomendacion_juego,
se debe ejecutar la API en local.



## Deployment
Creé un repositorio especificamente optimizado para el deployment al cual se puede acceder mediante este [link](https://github.com/Abimael-Lib/P1_MLOPs_Steam_Games_Render).
