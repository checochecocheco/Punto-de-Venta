#%%
import tkinter as tk
from tkinter import messagebox

class PuntoDeVenta:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de Venta")

        # Variables para la interfaz
        self.productos = {"Producto1": 10.0, "Producto2": 15.0, "Producto3": 20.0}
        self.carrito = {}
        self.total = tk.DoubleVar()

        # Configurar la interfaz de usuario
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Lista desplegable para seleccionar el producto
        tk.Label(self.root, text="Producto:").grid(row=0, column=0)
        self.producto_var = tk.StringVar()
        self.producto_var.set(list(self.productos.keys())[0])  # Establecer el primer producto como valor inicial
        tk.OptionMenu(self.root, self.producto_var, *self.productos.keys()).grid(row=0, column=1)

        # Entrada para la cantidad
        tk.Label(self.root, text="Cantidad:").grid(row=1, column=0)
        self.cantidad_entry = tk.Entry(self.root)
        self.cantidad_entry.grid(row=1, column=1)

        # Botón para agregar productos al carrito
        tk.Button(self.root, text="Agregar al carrito", command=self.agregar_al_carrito).grid(row=2, column=0, columnspan=2)

        # Lista de productos en el carrito
        tk.Label(self.root, text="Carrito:").grid(row=3, column=0)
        self.carrito_listbox = tk.Listbox(self.root)
        self.carrito_listbox.grid(row=4, column=0, columnspan=2)

        # Etiqueta para mostrar el total
        tk.Label(self.root, text="Total:").grid(row=5, column=0)
        tk.Label(self.root, textvariable=self.total).grid(row=5, column=1)

        # Botón para finalizar la venta
        tk.Button(self.root, text="Finalizar venta", command=self.finalizar_venta).grid(row=6, column=0, columnspan=2)

    def agregar_al_carrito(self):
        producto_seleccionado = self.producto_var.get()
        cantidad = self.cantidad_entry.get()

        # Validar la entrada de cantidad
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        cantidad = int(cantidad)

        # Agregar el producto al carrito
        if producto_seleccionado in self.carrito:
            self.carrito[producto_seleccionado] += cantidad
        else:
            self.carrito[producto_seleccionado] = cantidad

        self.actualizar_carrito_y_total()

    def actualizar_carrito_y_total(self):
        # Actualizar la lista del carrito
        self.carrito_listbox.delete(0, tk.END)
        for producto, cantidad in self.carrito.items():
            self.carrito_listbox.insert(tk.END, f"{producto} x{cantidad}")

        # Calcular el total sumando los precios de los productos en el carrito
        precio_total = sum([self.productos[producto] * cantidad for producto, cantidad in self.carrito.items()])

        # Actualizar la variable total
        self.total.set(precio_total)

    def finalizar_venta(self):
        if self.carrito:
            messagebox.showinfo("Venta finalizada", f"Venta finalizada. Total: ${self.total.get():.2f}")
            self.root.destroy()
        else:
            messagebox.showwarning("Carrito vacío", "El carrito está vacío. No se puede finalizar la venta.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoDeVenta(root)
    root.mainloop()
#%%

'''
COMANDOS PARA  SQLITE

CREAR TABLA:

CREATE TABLE estudiantes (  #Nombre de la tabla
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    edad INTEGER,       #Nombre de la columna y tipo de dato
    promedio FLOAT      #
);


Insertar fatos:
INSERT INTO estudiantes (nombre, edad, promedio)
VALUES ('Carlos', 20, 85.5);

INSERT INTO estudiantes (nombre, edad, promedio)
VALUES ('Mario', 22, 90.0);

CONSULTA DE DATOS:
SELECT * FROM estudiantes;


ACTUALIZAR DATOS:
UPDATE estudiantes
SET promedio = 88.0
WHERE nombre = 'Juan';

PARA ELIMINAR DATOS
DELETE FROM estudiantes
WHERE nombre = 'María';


CONSULTA CONDICIONADAD
SELECT * FROM estudiantes
WHERE edad > 21;


AGG COLUMNA
ALTER TABLE estudiantes
ADD COLUMN carrera TEXT;

'''

#%%
import sqlite3

# Conectar a la base de datos (creará un archivo llamado "mi_base_de_datos.db" si no existe)
conexion = sqlite3.connect("mi_base_de_datos.db")

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Definir el comando SQL para crear una tabla llamada "estudiantes"
comando_sql = """
CREATE TABLE estudiant (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    edad INTEGER,
    promedio REAL
);
"""

# Ejecutar el comando SQL
cursor.execute(comando_sql)

# Confirmar los cambios y cerrar la conexión
conexion.commit()
print("Conexion exitosa")
conexion.close()
print("Cerrar")

# %%

def __init__(self, root, database_name="punto_de_venta.db"):
    self.root = root
    self.root.title("Blue and Yellow Company")
    self.conn = sqlite3.connect(database_name)  # Conexión BD
    self.c = self.conn.cursor()

    # Imprime la ubicación de la base de datos
    print(f"Ubicación de la base de datos: {os.path.abspath(database_name)}")

    # Resto del código...

