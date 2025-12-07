
import pandas as pd
print("✅ Pandas instalado!")
print("Versión:", pd.__version__)
df=pd.read_csv('src/clase01/productos.csv')
otro_df=pd.read_csv('src/clase01/otros_productos.csv')
# FUNCIONES BÁSICAS DE PANDAS


#/////////////////////////////////////
#/////////////////////////////////////
#/////////////////////////////////////

# Lectura y escritura de datos con Pandas
'''
pd.read_csv() #Leer archivos CSV
pd.read_excel() #Leer archivos Excel
pd.to_csv() #Guardar DataFrame en CSV
pd.to_excel() #Guardar DataFrame en Excel
pd.DataFrame() #Crear DataFrame desde diccionarios o listas
'''
#/////////////////////////////////////
#/////////////////////////////////////
#/////////////////////////////////////

# ### # SELECCIÓN DE DATOS EN PANDAS MEDIANTE `loc`, `iloc` Y NOMBRE DIRECTO #### 
'''
En Pandas existen **dos grandes formas de seleccionar datos**:
'''
## 1. Selección por POSICIÓN → `iloc` //df.iloc[] → por posición (números)
## 2. Selección por ETIQUETAS → `loc` //df.loc[]  → por etiquetas (nombres)
## 3. Selección por NOMBRE DIRECTO (solo columnas) // df[]  → selección simple de columnas

#---------------

## 1. Selección por POSICIÓN → `iloc`
# Se usa cuando quieres acceder por _índices numéricos_ (0, 1, 2…).
# Ejemplo: *fila 0, columna 2*

df.iloc[0]     # primera fila
df.iloc[0, 2] # Seleccionar fila y columna por índice
df.iloc[4, 1]
df.iloc[0:5]   # filas 0 a 4
df.iloc[:, [0, 2]]   # columnas 0 y 2

#----------

## **2. Selección por ETIQUETAS → `loc`**
# Se usa para acceder por el **nombre de filas o columnas**.
# Ejemplo: *fila con índice "A", columna "precio"*

df.loc['A']      # fila con índice 'A'
df.loc["A", "precio"]
df.loc[:, ['columna1', 'columna2']] #Seleccionar varias columnas por nombre
fila = 2
df.loc[fila, 'nombre_columna'] #Seleccionar un valor específico


# 3. Selección por NOMBRE DIRECTO (solo columnas)
# Cuando seleccionas una columna directamente:

### Para obtener **Series**
df['columna']

# Para obtener **DataFrame**
df[['columna']]
df[['col1', 'col2']]

# /////////////////////////////////////////7
# 🟣 4. Selección avanzada
### ✔ Usar condiciones (Boolean Masking)
df[df['edad'] > 30]
df[(df['edad'] > 30) & (df['ciudad'] == 'Bogotá')]

### ✔ Usar `isin`
# 'isin' permite filtrar filas según si una columna tiene valores dentro de una lista dada.
# En Excel es similar a: aplicar Filtro a la tabla por varios valores,
# o usar funciones como OR() y COUNTIF() para comprobar si un valor está en una lista.
df[df['categoria'].isin(['A', 'B', 'C'])]
### ✔ Selección por query
df.query("edad > 30 and ciudad == 'Bogotá'")

# Using .loc for label-based indexing
# Seleccionar filas donde 'edad' > 30 y mostrar solo 'nombre' y 'ciudad'
df.loc[df['edad'] > 30, ['nombre', 'ciudad']]
'''
se diferentcia de 'df[df['edad'] > 30][['nombre', 'ciudad']]' en que es más eficiente y claro al combinar filtrado y selección de columnas en una sola operación.  ?????
'''


#/////////////////////////////////////
#/////////////////////////////////////
#/////////////////////////////////////


# DIFERENCIA ENTRE DATAFRAME Y SERIES EN PANDAS
'''
Un **DataFrame** es una tabla completa (con filas y columnas).
Una **Series** es una única columna de un DataFrame.

Usar uno u otro depende de lo que necesites:
* Usa **DataFrame** cuando quieras trabajar con datos tabulares completos: filtrar filas, seleccionar varias columnas, agrupar, unir, ordenar, etc.
* DataFrame → si trabajas con **múltiples columnas**, análisis tabular, joins, groupby, filtros complejos.
* Usa **Series** cuando quieras trabajar directamente con los valores de una sola columna: estadísticas, valores únicos, funciones matemáticas, etc.
* Series → si trabajas con **una sola columna** y necesitas estadísticas, valores únicos, transformaciones matemáticas.
'''

#### SELECCIÓN Y USO DE DATAFRAME #### 

# Seleccionar una columna en formato DataFrame (devuelve DataFrame)
df[['columna']]

# Seleccionar varias columnas
df[['col1', 'col2', 'col3']]

# Filtrar FILAS basadas en una condición (devuelve DataFrame)
df[df['columna'] == 'valor']
df[df['monto'] > 1000] # Filtrar filas con monto mayor a 1000 <3
'''
Sintaxis propia, que permite operación vectorial de filtrado, aprovecha una técnica llamada "Indexación Booleana" para realizar filtros de manera vectorial y muy eficiente. y que devuelve un nuevo DataFrame con solo las filas que cumplen la condición.
'''
# Filtrar FILAS con varias condiciones
df[(df['edad'] > 18) & (df['ciudad'] == 'Bogotá')]

# Filtrar usando isin()
df[df['categoria'].isin(['A', 'B', 'C'])]

# Ordenar (devuelve DataFrame)
df.sort_values(by='precio', ascending=False)

# Renombrar columnas
df.rename(columns={"old": "new"})

# Resetear índice
df.reset_index(drop=True)

# Eliminar columnas
df.drop(columns=['columna'])

# Agrupar y calcular agregados
df.groupby('categoria')['monto'].sum()
df.groupby('categoria').agg({'monto':'sum', 'precio':'mean'})

# Unir DataFrames (merge)
df.merge(otro_df, on='id', how='left')

#-------

####  SELECCIÓN Y USO DE SERIES #### 

# Una serie es una sola columna:
df['columna']  # devuelve Series

# Valores únicos (Series)
df['columna'].unique()
'''Listar valores únicos en una columna (Resultado: Serie) '''

# Conteo de valores (Series)
df['columna'].value_counts()
'''#Contar ocurrencias de cada valor en una columna'''

# Acceder a un valor por índice
fila = 5
df['columna'][fila] # (Resultado: valor único)

# Estadísticas básicas
df['monto'].mean()
df['monto'].sum()
df['monto'].max()
df['monto'].min()
df['monto'].median()

# Convertir tipos
df['edad'].astype(int)
df['precio'].astype(float)

# Reemplazar valores
df['columna'].replace({'viejo': 'nuevo'})

# Aplicar funciones element-wise
df['precio'].apply(lambda x: x * 1.19)   # IVA por ejemplo

# Detectar valores nulos
df['columna'].isna().sum()
