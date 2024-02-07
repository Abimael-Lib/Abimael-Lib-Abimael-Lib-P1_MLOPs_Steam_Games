## Funciones utiles para el ETL y el EDA
# Librerias necesarias
import pandas as pd
from textblob import TextBlob
import re

# Funciones
def verificar_tipo_datos(df):
    '''
    Realiza un análisis de tipos de datos y la presencia de valores nulos en un DataFrame.
    
    Toma un DataFrame como entrada y devuelve un resumen que incluye información sobre tipos de datos 
    en cada columna, porcentaje de valores no nulos y nulos, así como la cantidad de valores nulos por columna. 
    
    El DataFrame resultante tiene las siguientes columnas: 
    'nombre_campo', 'tipo_datos', 'no_nulos_%', 'nulos_%', y 'nulos'.
    '''

    mi_dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
        mi_dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        mi_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        mi_dict["nulos"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(mi_dict)
        
    return df_info

def analisis_sentimiento(review):
    '''
    Realiza un análisis de sentimiento en un texto utilizando la librería TextBlob.
    
    Devuelve un valor numérico que representa el sentimiento del texto, donde 0 
    indica sentimiento negativo, 1 indica sentimiento neutral o no clasificable, 
    y 2 indica sentimiento positivo.
    '''
    if review is None:
        return 1
    analysis = TextBlob(review)
    polarity = analysis.sentiment.polarity
    if polarity < -0.2:
        return 0  
    elif polarity > 0.2: 
        return 2 
    else:
        return 1 
    
def ejemplos_review_por_sentimiento(reviews, sentiments):
    '''
    Imprime ejemplos de reviews para cada categoría de análisis de sentimiento. 
    
    Recibe dos listas paralelas: reviews, que contiene los textos de las reviews, y sentiments, 
    que contiene los valores de sentimiento correspondientes a cada review. 
    
    La función imprime ejemplos de reviews para cada categoría de sentimiento (0, 1, o 2).
    
    No devuelve ningún valor, simplemente imprime los ejemplos.
    '''
    for sentiment_value in range(3):
        print(f"Para la categoría de análisis de sentimiento {sentiment_value} se tienen estos ejemplos de reviews:")
        sentiment_reviews = [review for review, sentiment in zip(reviews, sentiments) if sentiment == sentiment_value]
        
        for i, review in enumerate(sentiment_reviews[:3], start=1):
            print(f"Review {i}: {review}")
        
        print("\n")

def verifica_duplicados_por_columna(df, columna):
    '''
    Verifica y muestra filas duplicadas en un DataFrame según una columna específica. 
    
    Toma un DataFrame y el nombre de una columna como entrada. 
    
    Identifica y filtra las filas duplicadas basadas en el contenido de la columna especificada, 
    las ordena para facilitar la comparación, y devuelve un DataFrame con las filas duplicadas 
    listas para su inspección y comparación. 
    
    Si no se encuentran duplicados, devuelve el mensaje "No hay duplicados".
    '''
    # Se filtran las filas duplicadas
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted

def obtener_anio_release(fecha):
    '''
    Extrae el año de una fecha en formato 'yyyy-mm-dd', manejando valores nulos. 
    
    Toma como entrada una fecha y devuelve el año si el dato es válido. 

    En caso de que la fecha sea nula o inconsistente, la función devuelve 'Dato no disponible'.
    '''
    if pd.notna(fecha):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return fecha.split('-')[0]
    return 'Dato no disponible'
    
def reemplaza_a_flotante(value):
    '''
    Reemplaza valores no numéricos y nulos en una columna con 0.0. 
    
    Toma un valor como entrada y trata de convertirlo a un número float. 
    
    Si la conversión es exitosa, el valor numérico se mantiene, en caso de
    que la conversión falle o si el valor es nulo, se devuelve 0.0 en su lugar. 
    
    La función retorna el valor numérico si la conversión es exitosa o nulo,
    y 0.0 si la conversión falla.
    '''
    if pd.isna(value):
        return 0.0
    try:
        float_value = float(value)
        return float_value
    except:
        return 0.0
    
def convertir_fecha(cadena_fecha):
    '''
    La función convierte una cadena de fecha en formato "Month Day, Year" 
    (por ejemplo, "October 5, 2020") a otro formato de fecha "YYYY-MM-DD". 
    
    Retorna la nueva cadena de fecha en el formato deseado o un mensaje 
    de error si la cadena no sigue el formato esperado.
    '''
    match = re.search(r'(\w+\s\d{1,2},\s\d{4})', cadena_fecha)
    if match:
        fecha_str = match.group(1)
        try:
            fecha_dt = pd.to_datetime(fecha_str)
            return fecha_dt.strftime('%Y-%m-%d')
        except:
            return 'Fecha inválida'
    else:
        return 'Formato inválido'

def resumen_cant_porcentaje(df, columna):
    '''
    Cuenta la cantidad de valores True/False en una columna específica de un 
    DataFrame y luego calcula el porcentaje correspondiente.
    
    Toma como parámetros el DataFrame (df) que contiene los datos y el nombre 
    de la columna (columna) para la cual se desea generar el resumen.
    
    El resultado es un nuevo DataFrame que resume la cantidad y el porcentaje 
    de True/False en la columna especificada.
    '''
    # Cuanta la cantidad de True/False luego calcula el porcentaje
    counts = df[columna].value_counts()
    percentages = round(100 * counts / len(df),2)
    # Crea un dataframe con el resumen
    df_results = pd.DataFrame({
        "Cantidad": counts,
        "Porcentaje": percentages
    })
    return df_results

def bigote_max(columna):
    '''
    Calcula el valor del bigote superior y la cantidad de valores atípicos en una
    columna específica de datos. Se le pasa como parámetro una columna (pandas.Series)
    y no devuelve ningún valor, sino que realiza el cálculo y posiblemente almacene 
    o imprima la información necesaria para comprender la presencia de valores atípicos 
    en la columna proporcionada.
    '''
    # Cuartiles
    q1 = columna.describe()[4]
    q3 = columna.describe()[6]

    # Valor del vigote
    bigote_max = round(q3 + 1.5*(q3 - q1), 2)
    print(f'El bigote superior de la variable {columna.name} se ubica en:', bigote_max)

    # Cantidad de atípicos

## Funciones utiles para el ETL y el EDA
# Librerias necesarias
import pandas as pd
from textblob import TextBlob
import re

# Funciones
def verificar_tipo_datos(df):
    '''
    Realiza un análisis de tipos de datos y la presencia de valores nulos en un DataFrame.
    
    Toma un DataFrame como entrada y devuelve un resumen que incluye información sobre tipos de datos 
    en cada columna, porcentaje de valores no nulos y nulos, así como la cantidad de valores nulos por columna. 
    
    El DataFrame resultante tiene las siguientes columnas: 
    'nombre_campo', 'tipo_datos', 'no_nulos_%', 'nulos_%', y 'nulos'.
    '''

    mi_dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
        mi_dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        mi_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        mi_dict["nulos"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(mi_dict)
        
    return df_info

def analisis_sentimiento(review):
    '''
    Realiza un análisis de sentimiento en un texto utilizando la librería TextBlob.
    
    Devuelve un valor numérico que representa el sentimiento del texto, donde 0 
    indica sentimiento negativo, 1 indica sentimiento neutral o no clasificable, 
    y 2 indica sentimiento positivo.
    '''
    if review is None:
        return 1
    analysis = TextBlob(review)
    polarity = analysis.sentiment.polarity
    if polarity < -0.2:
        return 0  
    elif polarity > 0.2: 
        return 2 
    else:
        return 1 
    
def ejemplos_review_por_sentimiento(reviews, sentiments):
    '''
    Imprime ejemplos de reviews para cada categoría de análisis de sentimiento. 
    
    Recibe dos listas paralelas: reviews, que contiene los textos de las reviews, y sentiments, 
    que contiene los valores de sentimiento correspondientes a cada review. 
    
    La función imprime ejemplos de reviews para cada categoría de sentimiento (0, 1, o 2).
    
    No devuelve ningún valor, simplemente imprime los ejemplos.
    '''
    for sentiment_value in range(3):
        print(f"Para la categoría de análisis de sentimiento {sentiment_value} se tienen estos ejemplos de reviews:")
        sentiment_reviews = [review for review, sentiment in zip(reviews, sentiments) if sentiment == sentiment_value]
        
        for i, review in enumerate(sentiment_reviews[:3], start=1):
            print(f"Review {i}: {review}")
        
        print("\n")

def verifica_duplicados_por_columna(df, columna):
    '''
    Verifica y muestra filas duplicadas en un DataFrame según una columna específica. 
    
    Toma un DataFrame y el nombre de una columna como entrada. 
    
    Identifica y filtra las filas duplicadas basadas en el contenido de la columna especificada, 
    las ordena para facilitar la comparación, y devuelve un DataFrame con las filas duplicadas 
    listas para su inspección y comparación. 
    
    Si no se encuentran duplicados, devuelve el mensaje "No hay duplicados".
    '''
    # Se filtran las filas duplicadas
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted

def obtener_anio_release(fecha):
    '''
    Extrae el año de una fecha en formato 'yyyy-mm-dd', manejando valores nulos. 
    
    Toma como entrada una fecha y devuelve el año si el dato es válido. 

    En caso de que la fecha sea nula o inconsistente, la función devuelve 'Dato no disponible'.
    '''
    if pd.notna(fecha):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return fecha.split('-')[0]
    return 'Dato no disponible'
    
def reemplaza_a_flotante(value):
    '''
    Reemplaza valores no numéricos y nulos en una columna con 0.0. 
    
    Toma un valor como entrada y trata de convertirlo a un número float. 
    
    Si la conversión es exitosa, el valor numérico se mantiene, en caso de
    que la conversión falle o si el valor es nulo, se devuelve 0.0 en su lugar. 
    
    La función retorna el valor numérico si la conversión es exitosa o nulo,
    y 0.0 si la conversión falla.
    '''
    if pd.isna(value):
        return 0.0
    try:
        float_value = float(value)
        return float_value
    except:
        return 0.0
    
def convertir_fecha(cadena_fecha):
    '''
    La función convierte una cadena de fecha en formato "Month Day, Year" 
    (por ejemplo, "October 5, 2020") a otro formato de fecha "YYYY-MM-DD". 
    
    Retorna la nueva cadena de fecha en el formato deseado o un mensaje 
    de error si la cadena no sigue el formato esperado.
    '''
    match = re.search(r'(\w+\s\d{1,2},\s\d{4})', cadena_fecha)
    if match:
        fecha_str = match.group(1)
        try:
            fecha_dt = pd.to_datetime(fecha_str)
            return fecha_dt.strftime('%Y-%m-%d')
        except:
            return 'Fecha inválida'
    else:
        return 'Formato inválido'

def resumen_cant_porcentaje(df, columna):
    '''
    Cuenta la cantidad de valores True/False en una columna específica de un 
    DataFrame y luego calcula el porcentaje correspondiente.
    
    Toma como parámetros el DataFrame (df) que contiene los datos y el nombre 
    de la columna (columna) para la cual se desea generar el resumen.
    
    El resultado es un nuevo DataFrame que resume la cantidad y el porcentaje 
    de True/False en la columna especificada.
    '''
    # Cuanta la cantidad de True/False luego calcula el porcentaje
    counts = df[columna].value_counts()
    percentages = round(100 * counts / len(df),2)
    # Crea un dataframe con el resumen
    df_results = pd.DataFrame({
        "Cantidad": counts,
        "Porcentaje": percentages
    })
    return df_results

def bigote_max(columna):
    '''
    Calcula el valor del bigote superior y la cantidad de valores atípicos en una
    columna específica de datos. Se le pasa como parámetro una columna (pandas.Series)
    y no devuelve ningún valor, sino que realiza el cálculo y posiblemente almacene 
    o imprima la información necesaria para comprender la presencia de valores atípicos 
    en la columna proporcionada.
    '''
    # Cuartiles
    q1 = columna.describe()[4]
    q3 = columna.describe()[6]

    # Valor del vigote
    bigote_max = round(q3 + 1.5*(q3 - q1), 2)
    print(f'El bigote superior de la variable {columna.name} se ubica en:', bigote_max)

    # Cantidad de atípicos
    print(f'Hay {(columna > bigote_max).sum()} valores atípicos en la variable {columna.name}')