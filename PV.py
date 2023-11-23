import tkinter as tk
from tkinter import messagebox
import sqlite3

class PuntoDeVenta:
    def __init__(self, root, database_name="punto_de_venta.db"):
        self.root = root
        self.root.title("Blue and Yellow Company")
        self.conn = sqlite3.connect(database_name)      #Conexion BD
        self.c = self.conn.cursor()
                                                
        self.c.execute('''                              
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY,
                nombre TEXT
            )
        ''')                        

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                precio REAL,
                proveedor_id INTEGER,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
            )
        ''')
        #Nombres
        self.proveedores = self.obtener_nombres_proveedores()
        self.productos = self.obtener_nombres_productos()
        self.carrito = {}               #Diccionario en el carrito
        self.total = tk.DoubleVar()    

        self.configurar_interfaz()      

    def configurar_interfaz(self):
        # Lista de seleccion de provedores
        tk.Label(self.root, text="Proveedor:").grid(row=0, column=0)        
        self.proveedor_var = tk.StringVar()
        self.proveedor_var.set(self.proveedores[0] if self.proveedores else "")  # Establecer el primer proveedor como valor inicial
        tk.OptionMenu(self.root, self.proveedor_var, *self.proveedores, command=self.actualizar_productos).grid(row=0, column=1) #Selecciona y actualiza los productos
        # Lista producto
        tk.Label(self.root, text="Producto:").grid(row=1, column=0)
        self.producto_var = tk.StringVar()
        self.producto_var.set(self.productos[0] if self.productos else "")  # Establecer el primer producto como valor inicial
        tk.OptionMenu(self.root, self.producto_var, *self.productos).grid(row=1, column=1)
        # Entrada para la cantidad
        tk.Label(self.root, text="Cantidad:").grid(row=2, column=0)
        self.cantidad_entry = tk.Entry(self.root)
        self.cantidad_entry.grid(row=2, column=1)
        # Agregar
        tk.Button(self.root, text="Agregar", command=self.agregar_al_carrito).grid(row=3, column=0, columnspan=2)
        # Lista del carrito
        tk.Label(self.root, text="Carrito:                   Item          Cantidad").grid(row=4, column=0)


        self.carrito_listbox = tk.Listbox(self.root)
        self.carrito_listbox.grid(row=5, column=0, columnspan=2)
        #Total
        tk.Label(self.root, text="Total:").grid(row=6, column=0)
        tk.Label(self.root, textvariable=self.total).grid(row=6, column=1) #Variable del tota
        #Venta
        tk.Button(self.root, text="Finalizar venta", command=self.finalizar_venta).grid(row=7, column=0, columnspan=2)



    def obtener_nombres_proveedores(self):
        self.c.execute("SELECT nombre FROM proveedores")        #Selecciona el proveedor
        return [nombre[0] for nombre in self.c.fetchall()]      #Recupera absolutamente todos los datos de la consulta

    def obtener_nombres_productos(self):
        self.c.execute("SELECT nombre FROM productos")          
        return [nombre[0] for nombre in self.c.fetchall()]      

    def actualizar_productos(self, *args):
        proveedor_seleccionado = self.proveedor_var.get()               #Selecciona el proveedor de la lista
        self.productos = self.obtener_nombres_productos_por_proveedor(proveedor_seleccionado)
        self.producto_var.set(self.productos[0] if self.productos else "")

    def obtener_nombres_productos_por_proveedor(self, proveedor):
        self.c.execute("SELECT nombre FROM productos WHERE proveedor_id=(SELECT id FROM proveedores WHERE nombre=?)", (proveedor,)) #obtiene el nombre
        return [nombre[0] for nombre in self.c.fetchall()]

    def agregar_al_carrito(self):
        producto_seleccionado = self.producto_var.get()     #Seleccion en la lista
        cantidad = self.cantidad_entry.get()

        # Contempla el error
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        cantidad = int(cantidad)        

        self.c.execute("SELECT precio FROM productos WHERE nombre=?", (producto_seleccionado,))
        precio_producto = self.c.fetchone()[0]

        # Agregar el producto al carrito
        if producto_seleccionado in self.carrito:
            self.carrito[producto_seleccionado]["cantidad"] += cantidad     #Cantidad
        else:
            self.carrito[producto_seleccionado] = {"cantidad": cantidad, "precio": precio_producto} #

        self.actualizar_carrito_y_total()

    def actualizar_carrito_y_total(self):
        self.carrito_listbox.delete(0, tk.END)
        for producto, detalles in self.carrito.items(): #Numero de elementos
            self.carrito_listbox.insert(tk.END, f"{producto}     {detalles['cantidad']}")

        # Multiplica
        precio_total = sum([detalles['precio'] * detalles['cantidad'] for detalles in self.carrito.values()])

        self.total.set(precio_total)

    def finalizar_venta(self):
        if self.carrito:
            messagebox.showinfo("Venta finalizada", f"Venta finalizada. Total: ${self.total.get():.2f}")
            self.root.destroy()
        else:
            messagebox.showwarning("Carrito vacío", "El carrito está vacío. No se puede finalizar la venta.")

    def __del__(self):
        # Fin de conexion de la BD
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoDeVenta(root)
    root.mainloop()
