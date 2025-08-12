from pydantic import BaseModel, Field

class ComposicionProdCompuesto(BaseModel):
    id_prodCompuesto: int = Field(..., description="ID del producto compuesto")
    id_componente: int = Field(..., description="ID del componente")
    cantidad: int = Field(..., gt=0, description="Cantidad del componente en el producto compuesto")

    class Config:
        orm_mode = True

class ComposicionProdCompuestoCreate(BaseModel):
    id_componente: int = Field(..., description="ID del componente")
    cantidad: int = Field(..., gt=0, description="Cantidad del componente en el producto compuesto")

    class Config:
        orm_mode = True