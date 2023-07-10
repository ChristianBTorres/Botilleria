class Producto():
    def __init__(self, nombre, precio, stock, proveedor):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.proveedor = proveedor

    def toDbCollection(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "proveedor": self.proveedor
        }


class Proveedor():
    def __init__(self, nombre, rut, telefono, correo, direccion):
        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def toDbCollection(self):
        return {
            "nombre": self.nombre,
            "rut": self.rut,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion
        }
