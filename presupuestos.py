import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime


class PresupuestoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Presupuestos")

        # Datos del presupuesto
        tk.Label(root, text="Cliente:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.cliente_entry = tk.Entry(root)
        self.cliente_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Moneda:").grid(
            row=0, column=2, padx=10, pady=5
        )
        self.moneda_var = tk.StringVar(value="Euros")
        self.moneda_menu = ttk.Combobox(
            root,
            textvariable=self.moneda_var,
            values=["Euros", "Dólares", "Pesos"],
            state="readonly"
        )
        self.moneda_menu.grid(row=0, column=3, padx=10, pady=5)
        self.moneda_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.update_tree()
        )

        tk.Label(root, text="Fecha:").grid(
            row=0, column=4, padx=10, pady=5
        )
        self.fecha_var = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        self.fecha_entry = tk.Entry(
            root,
            textvariable=self.fecha_var,
            state="readonly"
        )
        self.fecha_entry.grid(row=0, column=5, padx=10, pady=5)

        # Campos para agregar o editar artículos
        self.items_frame = tk.Frame(root)
        self.items_frame.grid(
            row=1, column=0, columnspan=8, padx=10, pady=5
        )

        tk.Label(self.items_frame, text="Descripción:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.desc_entry = tk.Entry(self.items_frame, width=22)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.items_frame, text="Cantidad:").grid(
            row=0, column=2, padx=5, pady=5
        )
        self.cant_entry = tk.Entry(self.items_frame, width=8)
        self.cant_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.items_frame, text="Precio unitario:").grid(
            row=0, column=4, padx=5, pady=5
        )
        self.pu_entry = tk.Entry(self.items_frame, width=12)
        self.pu_entry.grid(row=0, column=5, padx=5, pady=5)

        self.add_button = tk.Button(
            self.items_frame,
            text="Agregar ítem",
            command=self.add_item
        )
        self.add_button.grid(row=0, column=6, padx=5, pady=5)

        self.edit_button = tk.Button(
            self.items_frame,
            text="Guardar cambios",
            command=self.save_edit,
            state="disabled"
        )
        self.edit_button.grid(row=0, column=7, padx=5, pady=5)

        # Tabla
        columnas = (
            "Descripción",
            "Cantidad",
            "Precio unitario",
            "Subtotal"
        )
        self.tree = ttk.Treeview(
            root,
            columns=columnas,
            show="headings",
            height=10
        )

        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio unitario", text="Precio unitario")
        self.tree.heading("Subtotal", text="Subtotal")

        self.tree.column("Descripción", width=250)
        self.tree.column("Cantidad", width=100, anchor="center")
        self.tree.column("Precio unitario", width=150, anchor="e")
        self.tree.column("Subtotal", width=150, anchor="e")

        self.tree.grid(
            row=2, column=0, columnspan=6, padx=10, pady=5
        )
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.edit_item)

        # Eliminar
        self.eliminar_button = tk.Button(
            root,
            text="Eliminar seleccionado",
            command=self.delete_item
        )
        self.eliminar_button.grid(
            row=3, column=0, columnspan=6, padx=10, pady=5
        )

        # Total
        tk.Label(root, text="Total general:").grid(
            row=4, column=0, padx=10, pady=5
        )
        self.total_var = tk.StringVar(value="0.00 Euros")
        self.total_entry = tk.Entry(
            root,
            textvariable=self.total_var,
            state="readonly",
            width=20
        )
        self.total_entry.grid(row=4, column=1, padx=10, pady=5)

        # Guardar y cargar
        self.save_button = tk.Button(
            root,
            text="Guardar presupuesto",
            command=self.save_presupuesto
        )
        self.save_button.grid(
            row=4, column=2, columnspan=2, padx=10, pady=5
        )

        self.load_button = tk.Button(
            root,
            text="Cargar presupuesto",
            command=self.load_presupuesto
        )
        self.load_button.grid(
            row=4, column=4, columnspan=2, padx=10, pady=5
        )

        # Elementos: (descripción, cantidad, precio unitario, subtotal)
        self.items = []
        self.editing_index = None

    @staticmethod
    def parse_number(value):
        """Acepta números con punto o coma decimal."""
        return float(value.strip().replace(",", "."))

    def clear_fields(self):
        self.desc_entry.delete(0, tk.END)
        self.cant_entry.delete(0, tk.END)
        self.pu_entry.delete(0, tk.END)

    def cancel_edit(self):
        self.editing_index = None
        self.edit_button.config(state="disabled")
        self.add_button.config(state="normal")
        self.clear_fields()
        self.tree.selection_remove(self.tree.selection())

    def add_item(self):
        descripcion = self.desc_entry.get().strip()
        cantidad_texto = self.cant_entry.get().strip()
        precio_texto = self.pu_entry.get().strip()

        if not descripcion or not cantidad_texto or not precio_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa la descripción, la cantidad y el precio unitario."
            )
            return

        try:
            cantidad = int(cantidad_texto)
            precio = self.parse_number(precio_texto)

            if cantidad <= 0 or precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Dato inválido",
                "La cantidad debe ser un entero positivo y el precio debe ser un número válido."
            )
            return

        subtotal = cantidad * precio
        self.items.append((descripcion, cantidad, precio, subtotal))
        self.update_tree()
        self.clear_fields()

    def update_tree(self):
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)

        total = 0

        for descripcion, cantidad, precio, subtotal in self.items:
            total += subtotal
            self.tree.insert(
                "",
                tk.END,
                values=(
                    descripcion,
                    cantidad,
                    f"{precio:.2f} {self.moneda_var.get()}",
                    f"{subtotal:.2f} {self.moneda_var.get()}"
                )
            )

        self.total_var.set(
            f"{total:.2f} {self.moneda_var.get()}"
        )

    def on_select(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        indice = self.tree.get_children().index(seleccion[0])
        descripcion, cantidad, precio, _ = self.items[indice]

        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, descripcion)

        self.cant_entry.delete(0, tk.END)
        self.cant_entry.insert(0, str(cantidad))

        self.pu_entry.delete(0, tk.END)
        self.pu_entry.insert(0, str(precio))

    def edit_item(self, event=None):
        # Solo activa el modo de edición; no pregunta ni guarda todavía.
        seleccion = self.tree.selection()
        if not seleccion:
            return

        indice = self.tree.get_children().index(seleccion[0])
        self.editing_index = indice
        self.add_button.config(state="disabled")
        self.edit_button.config(state="normal")
        self.desc_entry.focus_set()

    def save_edit(self):
        if self.editing_index is None:
            return

        descripcion = self.desc_entry.get().strip()
        cantidad_texto = self.cant_entry.get().strip()
        precio_texto = self.pu_entry.get().strip()

        if not descripcion or not cantidad_texto or not precio_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa la descripción, la cantidad y el precio unitario."
            )
            return

        try:
            cantidad = int(cantidad_texto)
            precio = self.parse_number(precio_texto)

            if cantidad <= 0 or precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Dato inválido",
                "La cantidad debe ser un entero positivo y el precio debe ser un número válido."
            )
            return

        subtotal = cantidad * precio
        self.items[self.editing_index] = (
            descripcion,
            cantidad,
            precio,
            subtotal
        )

        indice = self.editing_index
        self.editing_index = None
        self.update_tree()
        self.clear_fields()
        self.edit_button.config(state="disabled")
        self.add_button.config(state="normal")

        elementos = self.tree.get_children()
        if indice < len(elementos):
            self.tree.selection_set(elementos[indice])

    def delete_item(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Sin selección",
                "Selecciona un artículo para eliminar."
            )
            return

        indice = self.tree.get_children().index(seleccion[0])
        self.items.pop(indice)
        self.cancel_edit()
        self.update_tree()

    def save_presupuesto(self):
        cliente = self.cliente_entry.get().strip()
        fecha = self.fecha_var.get()
        moneda = self.moneda_var.get()
        total = sum(item[3] for item in self.items)

        texto = (
            f"Cliente: {cliente}\n"
            f"Fecha: {fecha}\n"
            f"Moneda: {moneda}\n\n"
            "Descripción\tCantidad\tPrecio unitario\tSubtotal\n"
        )

        for descripcion, cantidad, precio, subtotal in self.items:
            texto += (
                f"{descripcion}\t{cantidad}\t{precio:.2f}\t"
                f"{subtotal:.2f} {moneda}\n"
            )

        texto += f"\nTotal general: {total:.2f} {moneda}\n"

        nombre_archivo = (
            f"{cliente or 'cliente'}_presupuesto_{fecha}.txt"
        )
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=nombre_archivo,
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(texto)

            messagebox.showinfo(
                "Presupuesto guardado",
                f"Presupuesto guardado en:\n{ruta}"
            )
        except OSError as error:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el archivo:\n{error}"
            )

    def load_presupuesto(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "r", encoding="utf-8-sig") as archivo:
                lineas = archivo.readlines()

            nuevos_items = []
            leyendo_items = False

            for linea_original in lineas:
                linea = linea_original.strip()

                if linea.startswith("Cliente:"):
                    cliente = linea.split(":", 1)[1].strip()
                    self.cliente_entry.delete(0, tk.END)
                    self.cliente_entry.insert(0, cliente)

                elif linea.startswith("Fecha:"):
                    self.fecha_var.set(
                        linea.split(":", 1)[1].strip()
                    )

                elif linea.startswith("Moneda:"):
                    self.moneda_var.set(
                        linea.split(":", 1)[1].strip()
                    )

                elif linea.startswith("Descripción"):
                    leyendo_items = True

                elif leyendo_items and linea:
                    partes = linea.split("\t")

                    if len(partes) != 4:
                        continue

                    descripcion = partes[0].strip()
                    if descripcion.startswith("Total general:"):
                        continue

                    cantidad = int(partes[1].strip())
                    precio = self.parse_number(partes[2])
                    subtotal = cantidad * precio

                    nuevos_items.append(
                        (descripcion, cantidad, precio, subtotal)
                    )

            self.items = nuevos_items
            self.cancel_edit()
            self.update_tree()

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Error al cargar",
                f"No se pudo leer el presupuesto:\n{error}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PresupuestoApp(root)
    root.mainloop()