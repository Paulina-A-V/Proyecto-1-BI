from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from estructura import DataModel, ReentrenamientoModel
from preprocesamiento import pipeline_datos

from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

import pandas as pd
from joblib import load, dump
import numpy as np


app = FastAPI()

# CONFIGURACIÓN DE CORS QUE PERMITE CONFIGURAR EL SERVIDOR WEB PARA PERMITIR SOLICITUDES DESDE DIFERENTES ORIGENES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el pipeline entrenado
model_path = "pipeline.joblib"
pipeline = load(model_path)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

def obtener_clasificaciones():
    df = pd.read_csv("../fake_news.csv", sep=";")
    df["clasificacion"] = df["Label"].apply(lambda x: "VERDADERO" if x == 1 else "FALSO")
    noticias = df[["Titulo", "Descripcion", "clasificacion"]].rename(columns={
        "Titulo": "titulo",
        "Descripcion": "noticia"
    })

    return noticias.to_dict(orient="records")


@app.get("/clasificaciones")
def obtener_clasificaciones_endpoint():
    return obtener_clasificaciones()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_prediction(dataModel: DataModel):
    # Convertir la entrada del modelo a DataFrame
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys())

    # Usar el pipeline cargado para hacer la predicción
    predictions = pipeline.predict(df).tolist()  # predecir todas las instancias
    probabilities = pipeline.predict_proba(df).tolist()  #  probabilidad de esa predicción

    # Devolver todas las predicciones y probabilidades
    return {"predictions": predictions, "probabilities": probabilities}

@app.post("/reentrenamiento")
def reentrenar_modelo(data: ReentrenamientoModel):
    textos_nuevos = data.Descripcion
    etiquetas_nuevas = data.Label

    if len(textos_nuevos) != len(etiquetas_nuevas):
        raise HTTPException(status_code=400, detail="El número de descripciones y labels no coincide")

    # Cargar el dataset original
    data_original = pd.read_csv("./fake_news.csv", sep=";")
    textos_originales = data_original['Descripcion']
    etiquetas_originales = data_original['Label']

    # Combinar los datos originales con los nuevos
    textos_combinados = pd.concat([textos_originales, pd.Series(textos_nuevos)], ignore_index=True)
    etiquetas_combinadas = pd.concat([etiquetas_originales, pd.Series(etiquetas_nuevas)], ignore_index=True)

    # Crear el DataFrame con las descripciones y labels combinados
    df = pd.DataFrame({'Descripcion': textos_combinados, 'Label': etiquetas_combinadas})

    # Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(
        df['Descripcion'], df['Label'], test_size=0.2, random_state=42, stratify=df['Label']
    )

    pipeline_copy = pipeline
    pipeline_copy.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = pipeline_copy.predict(X_test)

    # Calcular las métricas de desempeño
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # Formatear las métricas a 5 cifras decimales
    precision = "{0:.5f}".format(precision)
    recall = "{0:.5f}".format(recall)
    f1 = "{0:.5f}".format(f1)

    # Guardar el modelo actualizado
    dump(pipeline_copy, model_path)

    return {
        "message": "Modelo reentrenado correctamente",
        "metrics": {
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }
    }