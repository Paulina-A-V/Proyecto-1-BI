from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):

    # Permite que la librería entienda la estructura de datos que va a recibir y pueda hacer el parseo de los datos.
    Descripcion: List[str]

    def columns(self):
        return ["Descripcion"]

#Pydantic (BaseModel) ayuda a asegurar que los datos que se reciben y se envían en la aplicación tengan el formato correcto
class ReentrenamientoModel(BaseModel):
    Descripcion: List[str]
    Label: List[int]

    def columns(self):
        return ["Descripcion", "Label"]