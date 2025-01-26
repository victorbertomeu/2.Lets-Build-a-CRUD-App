import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Configuración de la base de datos
def init_db():
    connection = sqlite3.connect("database/crud_app.db")
    cursor = connection.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL
        )
    """)
    connection.commit()
    connection.close()

# Función para añadir un ítem
def add_item(name, description, quantity, price):
    try:
        connection = sqlite3.connect("database/crud_app.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO items (name, description, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (name, description, quantity, price))

        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error al añadir el ítem:", e)
        return False

# Función para obtener todos los ítems
def get_items():
    try:
        connection = sqlite3.connect("database/crud_app.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()

        connection.close()
        return rows
    except Exception as e:
        print("Error al obtener los ítems:", e)
        return []

# Función para actualizar un ítem
def update_item(item_id, name, description, quantity, price):
    try:
        connection = sqlite3.connect("database/crud_app.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE items
            SET name = ?, description = ?, quantity = ?, price = ?
            WHERE id = ?
        """, (name, description, quantity, price, item_id))

        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error al actualizar el ítem:", e)
        return False

# Función para eliminar un ítem
def delete_item(item_id):
    try:
        connection = sqlite3.connect("database/crud_app.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))

        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error al eliminar el ítem:", e)
        return False

# Crear la ventana principal
def main_window():
    window = tk.Tk()
    window.title("CRUD App - Tkinter y SQLite")
    window.geometry("800x600")

    # Etiqueta de bienvenida
    label = tk.Label(window, text="¡Bienvenido a la aplicación CRUD!", font=("Arial", 16))
    label.pack(pady=10)

    # Tabla de ítems
    columns = ("id", "name", "description", "quantity", "price")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.capitalize())
    tree.pack(pady=10)

    # Cargar ítems en la tabla
    def load_items():
        for row in tree.get_children():
            tree.delete(row)
        for item in get_items():
            tree.insert("", tk.END, values=item)

    load_items()

    # Formulario de entrada
    tk.Label(window, text="Nombre:").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Descripción:").pack()
    description_entry = tk.Entry(window)
    description_entry.pack()

    tk.Label(window, text="Cantidad:").pack()
    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    tk.Label(window, text="Precio:").pack()
    price_entry = tk.Entry(window)
    price_entry.pack()

    # Botón para añadir ítem
    def handle_add_item():
        name = name_entry.get()
        description = description_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            success = add_item(name, description, int(quantity), float(price))
            if success:
                messagebox.showinfo("Éxito", "Ítem añadido correctamente")
                name_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                load_items()
            else:
                messagebox.showerror("Error", "No se pudo añadir el ítem")
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa los campos correctamente")

    tk.Button(window, text="Añadir Ítem", command=handle_add_item).pack(pady=5)

    # Botón para actualizar ítem
    def handle_update_item():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un ítem para actualizar")
            return

        item = tree.item(selected, "values")
        item_id = item[0]

        name = name_entry.get()
        description = description_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            success = update_item(item_id, name, description, int(quantity), float(price))
            if success:
                messagebox.showinfo("Éxito", "Ítem actualizado correctamente")
                load_items()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el ítem")
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa los campos correctamente")

    tk.Button(window, text="Actualizar Ítem", command=handle_update_item).pack(pady=5)

    # Botón para eliminar ítem
    def handle_delete_item():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un ítem para eliminar")
            return

        item = tree.item(selected, "values")
        item_id = item[0]

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este ítem?")
        if confirm:
            success = delete_item(item_id)
            if success:
                messagebox.showinfo("Éxito", "Ítem eliminado correctamente")
                load_items()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ítem")

    tk.Button(window, text="Eliminar Ítem", command=handle_delete_item).pack(pady=5)

    # Botón de salida
    tk.Button(window, text="Salir", command=window.destroy).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    # Inicializar la base de datos
    init_db()

    # Mostrar la ventana principal
    main_window()