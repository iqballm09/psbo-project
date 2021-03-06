# Import libraries
from ezeats import schemas, models, cbv
from ezeats.database import get_db, engine
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, status, HTTPException, APIRouter

# Initiate app and router
app = FastAPI()
router = APIRouter(
    prefix="/resto",
    tags=["Resto"]
)
models.Base.metadata.create_all(engine)


@cbv.cbv(router)
class Resto:
    session: Session = Depends(get_db)
    
    ## Create
    @router.post("/", status_code=status.HTTP_201_CREATED)
    def create(self, item: schemas.Resto):
        new_item = models.Resto(nama = item.nama ,
                                kategori = item.kategori ,
                                harga = item.harga
                                jam_buka = item.jam_buka ,
                                jam_tutup = item.jam_tutup ,
                                fasilitas = item.fasilitas ,
                                deskripsi = item.deskripsi ,
                                jalan = item.jalan ,
                                kecamatan = item.kecamatan ,
                                kotakab = item.kotakab ,
                                nama_kabkota = item.nama_kabkota ,
                                provinsi = item.provinsi ,
                                web = item.web ,
                                foto_menu = item.foto_menu ,
                                foto_cover = item.foto_cover ,
                                foto_resto = item.foto_resto ,
                                no_telp = item.no_telp )
        self.session.add(new_item)
        self.session.commit()          
        return f'Resto berhasil ditambahkan'

    ## Read
    @router.get('/')
    def show_all(self):
        list_resto = self.session.query(models.Resto).all()
        return list_resto    
    
    @router.get('/{id}', status_code=status.HTTP_200_OK)
    def show_by_id(self, id):
        resto = self.session.query(models.Resto).filter(models.Resto.id == id).first()
        if not resto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Restoran dengan id = {id} tidak ada")
        return resto

    ## Update
    @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
    def update(self, id, request: schemas.Resto):
        resto = self.session.query(models.Resto).filter(models.Resto.id == id).first()
        if not resto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Resto dengan id = {id} tidak ditemukan")
        resto.update(request.dict())                                                           
        self.session.commit()
        self.session.refresh(resto)
        return resto   

    ## Delete
    @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
    def destroy(self, id):
        resto = self.session.query(models.Resto).filter(models.Resto.id == id).delete(synchronize_session=False)
        self.session.commit()
        if not resto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Restoran dengan id = {id} tidak ada")           
        return f"Restoran berhasil dihapus"


app.include_router(router)
