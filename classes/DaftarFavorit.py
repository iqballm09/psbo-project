from classes.KoleksiSaya import KoleksiSaya

class DaftarFavorit(KoleksiSaya):
    def __init__(self, id, status, jam, tanggal):
        super().__init__(id, status, jam, tanggal)