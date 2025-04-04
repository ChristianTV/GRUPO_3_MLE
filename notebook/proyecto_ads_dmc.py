# -*- coding: utf-8 -*-
"""Proyecto ADS_DMC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JMCFC2rF1odsHlLgs96EU2Uxe1xzzYX1

# 1. Análisis del Caso

# 2. Preprocesamiento y Análisis Exploratorio de Datos (EDA)

## 2.1. Configuración e Importación de Librerías
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %matplotlib inline
plt.style.use('default')

"""## 2.2. Carga de Datos"""

train = pd.read_csv('train.csv', parse_dates=['Date'], dayfirst=True)
store = pd.read_csv('store.csv')
test = pd.read_csv('test.csv', parse_dates=['Date'], dayfirst=True)
sample_submission = pd.read_csv('sample_submission.csv')

print("Primeras filas de train.csv:")
display(train.head())

print("Primeras filas de store.csv:")
display(store.head())

print("Primeras filas de test.csv:")
display(test.head())

print("Primeras filas de sample_submission.csv:")
display(sample_submission.head())

"""## 2.3. Inspección General y Análisis de Valores Nulos"""

print("Información general de train.csv:")
train.info()
print("\nValores nulos en train.csv:")
display(train.isnull().sum())

# Información general y chequeo de valores nulos en store.csv
print("\nInformación general de store.csv:")
store.info()
print("\nValores nulos en store.csv:")
display(store.isnull().sum())

# Información general y chequeo de valores nulos en test.csv
print("\nInformación general de test.csv:")
test.info()
print("\nValores nulos en test.csv:")
display(test.isnull().sum())

"""### 1. Imputación en store.csv

- Para CompetitionDistance: Es razonable usar la mediana, ya que es robusta frente a outliers.
- Para CompetitionOpenSinceMonth y CompetitionOpenSinceYear: Si un valor es nulo puede interpretarse como que no existe competencia (o no se conoce), así que se puede rellenar con 0.
- Para Promo2SinceWeek y Promo2SinceYear: Rellenar con 0 si se entiende que no participa en Promo2.
- Para PromoInterval: Asignar "None" para indicar que no hay promoción continua.
"""

# Imputación de valores nulos en store.csv
store['CompetitionDistance'].fillna(store['CompetitionDistance'].median(), inplace=True)
store['CompetitionOpenSinceMonth'].fillna(0, inplace=True)
store['CompetitionOpenSinceYear'].fillna(0, inplace=True)
store['Promo2SinceWeek'].fillna(0, inplace=True)
store['Promo2SinceYear'].fillna(0, inplace=True)
store['PromoInterval'].fillna("None", inplace=True)

"""### 2. Imputación en test.csv

- Se asume que en esos casos la tienda estuvo abierta (o se tiene otro criterio de negocio), rellenando con 1
"""

# Imputación de valores nulos en test.csv
test['Open'].fillna(1, inplace=True)

"""### 3. Validación de no-vacíos"""

print("Información general de train.csv:")
train.info()
print("\nValores nulos en train.csv:")
display(train.isnull().sum())

# Información general y chequeo de valores nulos en store.csv
print("\nInformación general de store.csv:")
store.info()
print("\nValores nulos en store.csv:")
display(store.isnull().sum())

# Información general y chequeo de valores nulos en test.csv
print("\nInformación general de test.csv:")
test.info()
print("\nValores nulos en test.csv:")
display(test.isnull().sum())

"""## 2.4. Análisis Descriptivo de las Ventas

### Estadísticas Descriptivas
"""

# Estadísticas descriptivas de la columna Sales en train.csv
print("Estadísticas descriptivas de Sales:")
display(train['Sales'].describe())

"""### Distribución de Ventas"""

# Histograma de las ventas
plt.figure(figsize=(15, 5))
plt.hist(train['Sales'], bins=50, edgecolor='black')
plt.title('Distribución de Ventas')
plt.xlabel('Ventas')
plt.ylabel('Frecuencia')
plt.show()

"""## 2.5. Análisis Temporal de las Ventas"""

# Agrupamos las ventas diarias y las sumamos para obtener el total de ventas por día
ventas_diarias = train.groupby('Date')['Sales'].sum()

plt.figure(figsize=(15, 5))
plt.plot(ventas_diarias.index, ventas_diarias.values)
plt.title('Ventas Totales Diarias')
plt.xlabel('Fecha')
plt.ylabel('Ventas Totales')
plt.xticks(rotation=45)
plt.show()

"""## 2.6. Análisis de Ventas por Día de la Semana"""

# Cálculo del promedio de ventas por día de la semana
ventas_por_dia = train.groupby('DayOfWeek')['Sales'].mean()

plt.figure(figsize=(8, 4))
ventas_por_dia.plot(kind='bar', edgecolor='black')
plt.title('Ventas Promedio por Día de la Semana')
plt.xlabel('Día de la Semana (1: Lunes, 7: Domingo)')
plt.ylabel('Ventas Promedio')
plt.show()

"""## 2.7. Efecto de las Promociones en las Ventas"""

# Separación de ventas con y sin promoción
ventas_con_promo = train[train['Promo'] == 1]['Sales']
ventas_sin_promo = train[train['Promo'] == 0]['Sales']

plt.figure(figsize=(15, 5))
plt.hist([ventas_con_promo, ventas_sin_promo], bins=50, edgecolor='black', label=['Con Promo', 'Sin Promo'])
plt.title('Comparación de Ventas: Con y Sin Promoción')
plt.xlabel('Ventas')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()

"""## 2.8. Relación entre Clientes y Ventas"""

plt.figure(figsize=(15, 5))
plt.scatter(train['Customers'], train['Sales'], alpha=0.5)
plt.title('Relación entre Número de Clientes y Ventas')
plt.xlabel('Número de Clientes')
plt.ylabel('Ventas')
plt.show()

"""## 2.9. Integración de Información de Tiendas"""

# Unimos el dataset de entrenamiento con el de tiendas utilizando la columna 'Store'
train_full = pd.merge(train, store, on='Store', how='left')

# Visualizamos las primeras filas del dataset resultante
print("Primeras filas del dataset integrado (train_full):")
display(train_full.head())

# Revisión de nulos en el DataFrame integrado train_full
print("Nulos en train_full:")
display(train_full.isnull().sum())

# Rellenar los nulos que puedan haber quedado en train_full
train_full.fillna({
    'CompetitionDistance': train_full['CompetitionDistance'].median(),
    'CompetitionOpenSinceMonth': 0,
    'CompetitionOpenSinceYear': 0,
    'Promo2SinceWeek': 0,
    'Promo2SinceYear': 0,
    'PromoInterval': 'None'
}, inplace=True)

"""# 3. FEATURE ENGINEERING Y ENCODING

## 3.0. Fusionar la información de 'store' con 'train' y 'test'
"""

train_full = pd.merge(train, store, on='Store', how='left')
test_full = pd.merge(test, store, on='Store', how='left')

"""## 3.1. Extracción de Características a partir de la Fecha"""

# 3.1. Función para extraer características de fecha
def extract_date_features(df):
    # Extraemos año, mes, día y semana del año a partir de la columna 'Date'
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
    # Creamos la variable 'IsWeekend': 1 si el día corresponde a sábado o domingo, 0 de lo contrario
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x in [6, 7] else 0)
    return df

# Aplicamos la función a ambos DataFrames
train_full = extract_date_features(train_full)
test_full = extract_date_features(test_full)

"""## 3.2. Función para agregar características de la competencia"""

# 3.2. Función para agregar características de la competencia
def add_competition_features(df):
    # Creamos la fecha de apertura de la competencia utilizando el mes y año (se asume el día 1)
    # Convertimos las columnas a enteros
    df['CompetitionOpenDate'] = pd.to_datetime(
        dict(year=df['CompetitionOpenSinceYear'].astype(int),
             month=df['CompetitionOpenSinceMonth'].astype(int),
             day=1),
        errors='coerce'
    )
    # Calculamos el tiempo (en meses) que la competencia ha estado abierta
    # Usamos la diferencia en días dividida por 30 (aproximación)
    df['CompetitionTimeOpen'] = ((df['Date'] - df['CompetitionOpenDate']).dt.days / 30).apply(lambda x: x if x > 0 else 0)
    return df

# Aplicamos la función a ambos DataFrames
train_full = add_competition_features(train_full)
test_full = add_competition_features(test_full)

"""## 3.3. Función para agregar características de Promo2"""

# 3.3. Función para agregar características de Promo2
def add_promo2_features(df):
    # Se asume que si no participa en Promo2 o los valores son 0, la promoción no ha iniciado.
    # Se crea la fecha de inicio de Promo2 concatenando 'Promo2SinceYear' y 'Promo2SinceWeek'
    # Se formatea de manera que la semana corresponda al lunes de esa semana.
    # Convertimos a enteros y luego a string para la concatenación.
    df['Promo2StartDate'] = pd.to_datetime(
        df['Promo2SinceYear'].astype(int).astype(str) + '-' +
        df['Promo2SinceWeek'].astype(int).astype(str) + '-1',
        format='%Y-%W-%w',
        errors='coerce'
    )
    # Calculamos el tiempo en semanas que lleva activa Promo2 (diferencia en días dividida por 7)
    df['Promo2Time'] = ((df['Date'] - df['Promo2StartDate']).dt.days / 7).apply(lambda x: x if x > 0 else 0)
    return df

# Aplicamos la función a ambos DataFrames
train_full = add_promo2_features(train_full)
test_full = add_promo2_features(test_full)

"""## 3.4. Encoding de variables categóricas

Las variables categóricas que vamos a transformar son:
- 'StateHoliday': Valores como '0', 'a', 'b', 'c'
- 'StoreType': (e.g., a, b, c, d)
- 'Assortment': (e.g., a, b, c)
- 'PromoInterval': (e.g., "None", "Jan,Apr,Jul,Oct")
Usaremos one-hot encoding para transformar estas columnas en variables dummy.
"""

categorical_cols = ['StateHoliday', 'StoreType', 'Assortment', 'PromoInterval']

# Aplicamos get_dummies a train_full
train_full_encoded = pd.get_dummies(train_full, columns=categorical_cols, drop_first=True)

# Hacemos lo mismo con test_full
test_full_encoded = pd.get_dummies(test_full, columns=categorical_cols, drop_first=True)

# Es posible que al codificar se generen diferentes columnas entre train y test.
# Alineamos las columnas de ambos DataFrames para que tengan las mismas variables.
train_full_encoded, test_full_encoded = train_full_encoded.align(test_full_encoded, join='outer', axis=1, fill_value=0)

# Verificamos que la transformación se realizó correctamente
print("Columnas del DataFrame de entrenamiento después del encoding:")
print(train_full_encoded.columns)
print("\nColumnas del DataFrame de test después del encoding:")
print(test_full_encoded.columns)

# Ya tenemos los DataFrames 'train_full_encoded' y 'test_full_encoded' listos para el modelado.

"""# 4. Selección y Entrenamiento de Modelos

## 4.1. Selección de Variables y División de los Datos
"""

# Lista de columnas a excluir (por ejemplo, la variable target, identificadores, fechas y variables derivadas que no se usan directamente)
exclude_cols = ['Sales', 'Customers', 'Date', 'CompetitionOpenDate', 'Promo2StartDate']

# Seleccionamos las columnas de train_full_encoded que usaremos para el modelado
features_columns = [col for col in train_full_encoded.columns if col not in exclude_cols]
target = 'Sales'

# Definimos X (features) e y (target)
X_model = train_full_encoded[features_columns]
y_model = train_full_encoded[target]

# Dividimos los datos en conjunto de entrenamiento y validación (80%/20%)
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X_model, y_model, test_size=0.2, random_state=42)

# Comprobamos que no haya valores nulos en X_train (todo debe ser numérico después del encoding)
print("Nulos en X_train:")
display(X_train.isnull().sum())

"""## 4.2. Evaluar Modelos Individuales

Evaluar Modelo 1: Regresión Lineal
"""

from sklearn.linear_model import LinearRegression

# Entrenamiento y predicción con Regresión Lineal
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_val)
rmspe_lr = rmspe(y_val, lr_pred)
print("RMSPE - Regresión Lineal: {:.4f}".format(rmspe_lr))

"""Evaluar Modelo 2: Random Forest"""

from sklearn.ensemble import RandomForestRegressor

# Entrenamiento y predicción con Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_val)
rmspe_rf = rmspe(y_val, rf_pred)
print("RMSPE - Random Forest: {:.4f}".format(rmspe_rf))

"""Evaluar Modelo 3: Gradient Boosting (sklearn)"""

from sklearn.ensemble import GradientBoostingRegressor

# Entrenamiento y predicción con Gradient Boosting (sklearn)
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gbr.fit(X_train, y_train)
gbr_pred = gbr.predict(X_val)
rmspe_gbr = rmspe(y_val, gbr_pred)
print("RMSPE - Gradient Boosting (sklearn): {:.4f}".format(rmspe_gbr))

"""Evaluar Modelo 4: XGBoost"""

import xgboost as xgb

# Entrenamiento y predicción con XGBoost
xgbr = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, verbosity=0)
xgbr.fit(X_train, y_train)
xgb_pred = xgbr.predict(X_val)
rmspe_xgb = rmspe(y_val, xgb_pred)
print("RMSPE - XGBoost: {:.4f}".format(rmspe_xgb))

"""Evaluar Modelo 5: LightGBM"""

# Le tuve que meter toda esta primera parte porque encontraba caracteres especiales xd validen si está bien, me dio pereza revisar

# Función para limpiar los nombres de las columnas
def clean_column_names(df):
    df.columns = [col.replace(',', '_').replace(' ', '_') for col in df.columns]
    return df

# Después de aplicar get_dummies y alinear los DataFrames, limpia los nombres:
train_full_encoded = pd.get_dummies(train_full, columns=categorical_cols, drop_first=True)
test_full_encoded = pd.get_dummies(test_full, columns=categorical_cols, drop_first=True)

# Alineamos ambos DataFrames para que tengan las mismas columnas
train_full_encoded, test_full_encoded = train_full_encoded.align(test_full_encoded, join='outer', axis=1, fill_value=0)

# Limpiamos los nombres de las columnas
train_full_encoded = clean_column_names(train_full_encoded)
test_full_encoded = clean_column_names(test_full_encoded)

# Ahora procedemos a la división para el modelado
# Excluimos columnas que no usaremos para la predicción (por ejemplo, target, fechas, etc.)
exclude_cols = ['Sales', 'Customers', 'Date', 'CompetitionOpenDate', 'Promo2StartDate']
features_columns = [col for col in train_full_encoded.columns if col not in exclude_cols]
target = 'Sales'

X_model = train_full_encoded[features_columns]
y_model = train_full_encoded[target]

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X_model, y_model, test_size=0.2, random_state=42)

# Entrenamiento con LightGBM utilizando callbacks para early stopping
import lightgbm as lgb

lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_val = lgb.Dataset(X_val, label=y_val, reference=lgb_train)

params = {
    'objective': 'regression',
    'metric': 'rmse',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'verbose': -1
}

lgb_model = lgb.train(
    params,
    lgb_train,
    num_boost_round=1000,
    valid_sets=[lgb_train, lgb_val],
    callbacks=[lgb.early_stopping(stopping_rounds=50), lgb.log_evaluation(100)]
)

lgb_pred = lgb_model.predict(X_val, num_iteration=lgb_model.best_iteration)
rmspe_lgb = rmspe(y_val, lgb_pred)
print("RMSPE - LightGBM: {:.4f}".format(rmspe_lgb))

"""## 4.3. Comparación de los Modelos"""

import pandas as pd

# Diccionario para almacenar los resultados
resultados = {
    "Regresión Lineal": rmspe_lr,
    "Random Forest": rmspe_rf,
    "Gradient Boosting (sklearn)": rmspe_gbr,
    "XGBoost": rmspe_xgb,
    "LightGBM": rmspe_lgb
}

# Convertir el diccionario en un DataFrame y ordenar según el RMSPE (de menor a mayor)
resultados_df = pd.DataFrame(list(resultados.items()), columns=["Modelo", "RMSPE"])
resultados_df.sort_values(by="RMSPE", inplace=True)
print("Comparación de Modelos (RMSPE):")
display(resultados_df)