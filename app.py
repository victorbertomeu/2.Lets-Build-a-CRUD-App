import sqlite3
import tkinter as tk
from tkinter import messagebox

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

# Crear la ventana principal
def main_window():
    window = tk.Tk()
    window.title("CRUD App - Tkinter y SQLite")
    window.geometry("600x400")

    # Etiqueta de bienvenida
    label = tk.Label(window, text="¡Bienvenido a la aplicación CRUD!", font=("Arial", 16))
    label.pack(pady=20)

    # Formulario de creación
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

    # Botón para añadir el ítem
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
            else:
                messagebox.showerror("Error", "No se pudo añadir el ítem")
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa los campos correctamente")

    tk.Button(window, text="Añadir Ítem", command=handle_add_item).pack(pady=10)

    # Botón de salida
    exit_button = tk.Button(window, text="Salir", command=window.destroy)
    exit_button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    # Inicializar la base de datos
    init_db()

    # Mostrar la ventana principal
    main_window()