import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

def cargar_datos(archivo):
    return pd.read_excel(archivo)

def procesar_datos(df):
    df['SEXO'] = df['SEXO'].map({'MASCULINO': 0, 'FEMENINO': 1})
    df['DIABETES'] = df['DIABETES'].map({'NO': 0, 'SI': 1})
    return df

def preparar_conjuntos(df):
    X = df[['EDAD', 'SEXO', 'IMC', 'HEMOGLOBINA']]
    y = df['DIABETES']
    return train_test_split(X, y, test_size=0.3, random_state=42)

def entrenar_modelo(X_train, y_train):
    modelo = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_split=5,
        random_state=42
    )
    modelo.fit(X_train, y_train)
    return modelo

def evaluar_modelo(modelo, X_test, y_test):
    predicciones = modelo.predict(X_test)
    precision = accuracy_score(y_test, predicciones)
    print(f"Precisión del modelo: {precision:.2%}")
    return precision

def ejecutar_proceso_completo():
    datos_entrenamiento = cargar_datos('ENFERMERIA.xlsx')
    datos_procesados = procesar_datos(datos_entrenamiento)
    
    X_train, X_test, y_train, y_test = preparar_conjuntos(datos_procesados)
    modelo_entrenado = entrenar_modelo(X_train, y_train)
    
    resultado = evaluar_modelo(modelo_entrenado, X_test, y_test)
    return modelo_entrenado, resultado

if __name__ == "__main__":
    modelo_final, metrica = ejecutar_proceso_completo()
    
    datos_nuevos = cargar_datos('NUEVOS_DATOS.xlsx')
    datos_nuevos_procesados = procesar_datos(datos_nuevos)
    
    X_nuevos = datos_nuevos_procesados[['EDAD', 'SEXO', 'IMC', 'HEMOGLOBINA']]
    predicciones_finales = modelo_final.predict(X_nuevos)
    
    resultados_finales = datos_nuevos_procesados.copy()
    resultados_finales['PREDICCION_DIABETES'] = np.where(predicciones_finales == 1, 'SI', 'NO')
    resultados_finales.to_excel('PREDICCION_DIABETES.xlsx', index=False)