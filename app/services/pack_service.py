from typing import List
from fastapi import HTTPException
from app.services import get_PackService
from app.models.composicion_pack_model import ComposicionPack
from .BaseService import BaseService
from ..models.pack_model import Pack
from ..schemas.pack_schema import PackResponse, PackCreate, PackUpdate
from app.models.articulo_model import Articulo
from app.schemas.articulo_schema import ArticuloResponse
from app.schemas.composicion_pack_schema import ComposicionPackCreate, ComposicionPackResponse

class PackService(BaseService):
    def __init__(self, db):
        super().__init__(db, Pack, PackResponse)

    def obtener_articulos_por_pack(self, id_pack: int) -> List[ComposicionPackResponse]:
        """
        Obtiene los artículos que pertenecen a un pack por su ID.
        Args:
            id_pack (int): ID del pack.
        Returns:
            List[ComposicionPackResponse]: Lista de artículos en el pack.
        """
        pack_service = get_PackService()(self.db)
        pack = pack_service.obtener_por_id(id_pack)
        if not pack:
            raise HTTPException(status_code=404, detail=f"Pack con ID {id_pack} no encontrado.")
        composiciones = self.db.query(ComposicionPack).filter(ComposicionPack.id_pack == id_pack).all()
        if not composiciones:
            return []
        articulo_ids = [c.id_producto for c in composiciones]
        articulos = self.db.query(Articulo).filter(Articulo.id.in_(articulo_ids)).all()
        articulo_lookup = {a.id: a for a in articulos}
        return [
            ComposicionPackResponse(
                articulo=ArticuloResponse.model_validate(articulo_lookup[c.id_producto], from_attributes=True),
                cantidad=c.cantidad
            )
            for c in composiciones if c.id_producto in articulo_lookup
        ]

    def agregar_articulos_a_pack(self, id_pack: int, composiciones: List[ComposicionPackCreate]) -> dict:
        """
        Agrega artículos a un pack con cantidad.
        """
        pack_service = get_PackService()(self.db)
        if pack_service.obtener_por_id(id_pack) is None:
            raise HTTPException(status_code=404, detail=f"Pack con ID {id_pack} no encontrado.")

        existentes = self.db.query(ComposicionPack).filter(ComposicionPack.id_pack == id_pack).all()
        existentes_ids = {c.id_producto for c in existentes}
        if any(c.id_producto in existentes_ids for c in composiciones):
            raise HTTPException(status_code=400, detail="Uno o más artículos ya están asociados al pack.")

        for c in composiciones:
            nueva_composicion = ComposicionPack(id_pack=id_pack, id_producto=c.id_producto, cantidad=c.cantidad)
            self.db.add(nueva_composicion)
        self.db.commit()
        return {"detail": f"Artículos [{', '.join(str(c.id_producto) for c in composiciones)}] agregados al pack exitosamente."}

    def eliminar_articulos_de_pack(self, id_pack: int, articulos: list[int]) -> dict:
        """
        Elimina artículos de un pack.
        """
        existentes = self.db.query(ComposicionPack).filter(ComposicionPack.id_pack == id_pack).all()
        existentes_ids = {c.id_producto for c in existentes}
        if any(articulo_id not in existentes_ids for articulo_id in articulos):
            raise HTTPException(status_code=400, detail="Uno o más artículos no están asociados al pack.")

        for articulo_id in articulos:
            self.db.query(ComposicionPack).filter(
                ComposicionPack.id_pack == id_pack,
                ComposicionPack.id_producto == articulo_id
            ).delete()
        self.db.commit()
        return {"detail": f"Artículos [{', '.join(map(str, articulos))}] eliminados del pack exitosamente."}