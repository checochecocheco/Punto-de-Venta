import tkinter as tk
from tkinter import messagebox
import sqlite3

class PuntoDeVenta:
    def __init__(self, root, database_name="punto_de_venta.db"):
        self.root = root
        self.root.title("Blue and Yellow Company")
        self.conn = sqlite3.connect(database_name)
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

        self.proveedores = self.obtener_nombres_proveedores()
        self.productos = self.obtener_nombres_productos()
        self.carrito = {}       #Lista
        self.total = tk.DoubleVar()
        self.Iva_ = tk.DoubleVar()
        self.cambio = tk.DoubleVar()

        self.configurar_interfaz()

    def configurar_interfaz(self):      #Interfaz
        tk.Label(self.root, text="Proveedor:").grid(row=0, column=0)
        self.proveedor_var = tk.StringVar()
        self.proveedor_var.set(self.proveedores[0] if self.proveedores else "")
        tk.OptionMenu(self.root, self.proveedor_var, *self.proveedores, command=self.actualizar_productos).grid(row=0, column=1)

        tk.Label(self.root, text="Producto:").grid(row=1, column=0)     #Producto
        self.producto_var = tk.StringVar()                              #Variable de la etiqueta
        self.producto_var.set(self.productos[0] if self.productos else "")
        self.producto_var_menu = tk.OptionMenu(self.root, self.producto_var, "")    #Menu de los productos
        self.producto_var_menu.grid(row=1, column=1)

        tk.Label(self.root, text="Cantidad:").grid(row=2, column=0)         #Etiqueta de Cantidad
        self.cantidad_entry = tk.Entry(self.root)                           #Entrada
        self.cantidad_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Cantidad del pago:").grid(row=3, column=0)
        self.cantidad_pagada_entry = tk.Entry(self.root)
        self.cantidad_pagada_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Calcular Cambio", command=self.calcular_cambio).grid(row=4, column=1, columnspan=2)  #Bot Cambio
        tk.Button(self.root, text="Agregar", command=self.agregar_al_carrito).grid(row=4, column=0, columnspan=1)       #Bot Agregar

        tk.Label(self.root, text="Carrito:").grid(row=5, column=0)
        tk.Label(self.root, text="Item      Cantidad      Precio").grid(row=5, column=1)
        self.carrito_listbox = tk.Listbox(self.root)
        self.carrito_listbox.grid(row=6, column=0, columnspan=2)

        tk.Label(self.root, text="Subtotal:").grid(row=7, column=0)
        tk.Label(self.root, textvariable=self.total).grid(row=7, column=1, sticky='w')

        tk.Label(self.root, text="Total(IVA):").grid(row=8, column=0)
        tk.Label(self.root, textvariable=self.Iva_).grid(row=8, column=1, sticky='w')

        tk.Label(self.root, text="Cambio:").grid(row=9, column=0)
        tk.Label(self.root, textvariable=self.cambio).grid(row=9, column=1)

        tk.Button(self.root, text="Finalizar venta", command=self.finalizar_venta).grid(row=10, column=0, columnspan=2) #button de finalizar venta

    def obtener_nombres_proveedores(self):
        self.c.execute("SELECT nombre FROM proveedores")
        return [nombre[0] for nombre in self.c.fetchall()]

    def obtener_nombres_productos(self):
        self.c.execute("SELECT nombre FROM productos")
        return [nombre[0] for nombre in self.c.fetchall()]

    def actualizar_productos(self, *args):
        proveedor_seleccionado = self.proveedor_var.get()                                           #Elige el proveedor
        self.productos = self.obtener_nombres_productos_por_proveedor(proveedor_seleccionado)       #Obtiene el Nombre
        self.producto_var.set(self.productos[0] if self.productos else "")                          #Seleccion del producto 

        # Actualiza la lista de productos en el menú desplegable
        menu = self.producto_var_menu["menu"]
        menu.delete(0, "end")
        for producto in self.productos:
            menu.add_command(label=producto, command=tk._setit(self.producto_var, producto))

    def obtener_nombres_productos_por_proveedor(self, proveedor):           #Selecciona el id de cada producto
        self.c.execute("SELECT nombre FROM productos WHERE proveedor_id=(SELECT id FROM proveedores WHERE nombre=?)", (proveedor,))
        return [nombre[0] for nombre in self.c.fetchall()]

    def agregar_al_carrito(self):
        producto_seleccionado = self.producto_var.get()
        cantidad = self.cantidad_entry.get()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        cantidad = int(cantidad)

        self.c.execute("SELECT precio FROM productos WHERE nombre=?", (producto_seleccionado,))
        precio_producto = self.c.fetchone()[0]

        if producto_seleccionado in self.carrito:
            self.carrito[producto_seleccionado]["cantidad"] += cantidad
        else:
            self.carrito[producto_seleccionado] = {"cantidad": cantidad, "precio": precio_producto}

        self.actualizar_carrito_y_total()

    def actualizar_carrito_y_total(self):
        self.carrito_listbox.delete(0, tk.END)
        for producto, detalles in self.carrito.items():
            self.carrito_listbox.insert(tk.END, f"{producto}     {detalles['cantidad']}     ${detalles['precio']:.2f}")     #Anade datos de cada producto que este en la lista

        precio_total = sum([detalles['precio'] * detalles['cantidad'] for detalles in self.carrito.values()])
        Iva = precio_total * 1.16
        Iva = round(Iva,2)
        self.total.set(precio_total)
        self.Iva_.set(Iva)
        self.cambio.set(0)

    def calcular_cambio(self):
        try:
            cantidad_pagada = float(self.cantidad_pagada_entry.get())

            if cantidad_pagada < self.Iva_.get():
                messagebox.showerror("Error", "La cantidad pagada no puede ser menor que el total.")
                return

            cambio = round(cantidad_pagada - self.Iva_.get(),2)
            self.cambio.set(cambio)

            messagebox.showinfo("Cambio Calculado", f"El cambio es: ${cambio:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")

    def finalizar_venta(self):      #funcion del boton finalizar venta
        if self.carrito:
            cantidad_pagada = float(self.cantidad_pagada_entry.get())
            cambio = cantidad_pagada - self.Iva_.get()
            self.cambio.set(cambio)
            messagebox.showinfo("Venta finalizada", f"""Venta finalizada. Total: ${self.Iva_.get():.2f} Cambio: ${self.cambio.get():.2f}
                        """)
            #self.root.destroy()
        else:
            messagebox.showwarning("Carrito vacío", "El carrito está vacío. No se puede finalizar la venta.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoDeVenta(root)
    root.mainloop()
