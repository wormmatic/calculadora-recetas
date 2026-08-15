import tkinter as tk
from tkinter import ttk, messagebox

ingredientes = []

# Colores
BG = "#FDF6EC"
CARD = "#FFFFFF"
ORANGE = "#F39C12"
GREEN = "#27AE60"
TEXT = "#2C3E50"

# ==========================================================
# RECETAS PREDETERMINADAS
# ==========================================================
# Se agregan recetas con datos ya conocidos (nombre, cantidad
# original de personas e ingredientes) para que un usuario que
# no sabe cocinar también pueda usar la aplicación: solo elige
# una receta de la lista y el sistema calcula las proporciones
# automáticamente. Quien SÍ conoce su propia receta puede seguir
# usando la opción "Personalizada" e ingresar sus propios datos.
RECETAS_PREDETERMINADAS = {
    "Arroz con pollo (4 personas)": {
        "personas": 4,
        "ingredientes": [
            ("Arroz", 2, "tazas"),
            ("Pechuga de pollo", 500, "gramos"),
            ("Cebolla", 1, "unidades"),
            ("Chile dulce", 1, "unidades"),
            ("Ajo", 2, "unidades"),
            ("Consomé de pollo", 2, "cucharadas"),
            ("Aceite", 3, "cucharadas"),
            ("Zanahoria", 1, "unidades"),
        ],
    },
    "Espagueti a la boloñesa (4 personas)": {
        "personas": 4,
        "ingredientes": [
            ("Pasta espagueti", 400, "gramos"),
            ("Carne molida", 500, "gramos"),
            ("Salsa de tomate", 2, "tazas"),
            ("Cebolla", 1, "unidades"),
            ("Ajo", 2, "unidades"),
            ("Aceite de oliva", 2, "cucharadas"),
            ("Queso parmesano", 4, "cucharadas"),
        ],
    },
    "Ensalada César (4 personas)": {
        "personas": 4,
        "ingredientes": [
            ("Lechuga romana", 2, "unidades"),
            ("Pechuga de pollo", 300, "gramos"),
            ("Pan para crotones", 100, "gramos"),
            ("Queso parmesano", 4, "cucharadas"),
            ("Aderezo césar", 6, "cucharadas"),
        ],
    },
    "Pancakes (4 personas)": {
        "personas": 4,
        "ingredientes": [
            ("Harina de trigo", 2, "tazas"),
            ("Leche", 1.5, "tazas"),
            ("Huevos", 2, "unidades"),
            ("Azúcar", 3, "cucharadas"),
            ("Polvo de hornear", 1, "cucharadas"),
            ("Mantequilla derretida", 3, "cucharadas"),
        ],
    },
    "Personalizada (ingresar manualmente)": {
        "personas": None,
        "ingredientes": [],
    },
}


def agregar_ingrediente(nombre_val="", cantidad_val="", unidad_val="unidades"):
    fila = len(ingredientes)

    nombre = tk.Entry(frame_tabla, width=18, font=("Segoe UI", 10))
    nombre.grid(row=fila + 1, column=0, padx=5, pady=5)
    if nombre_val:
        nombre.insert(0, nombre_val)

    cantidad = tk.Entry(frame_tabla, width=10, font=("Segoe UI", 10))
    cantidad.grid(row=fila + 1, column=1, padx=5)
    if cantidad_val != "":
        cantidad.insert(0, cantidad_val)

    unidad = ttk.Combobox(
        frame_tabla,
        values=["gramos", "kg", "tazas", "cucharadas", "unidades", "litros"],
        width=12
    )
    unidad.grid(row=fila + 1, column=2, padx=5)
    unidad.set(unidad_val)

    ingredientes.append((nombre, cantidad, unidad))


def limpiar_filas_ingredientes():
    """Elimina del formulario todas las filas de ingredientes actuales."""
    for nombre, cantidad, unidad in ingredientes:
        nombre.destroy()
        cantidad.destroy()
        unidad.destroy()
    ingredientes.clear()


def cargar_receta_predeterminada(event=None):
    """Se ejecuta cuando el usuario elige una receta del combobox.
    Llena automáticamente el nombre, las personas originales y los
    ingredientes, para que el usuario no necesite conocerlos de antemano."""
    seleccion = combo_recetas.get()
    if seleccion not in RECETAS_PREDETERMINADAS:
        return

    receta = RECETAS_PREDETERMINADAS[seleccion]

    # Limpiar campos y filas actuales antes de cargar la nueva receta
    entry_receta.delete(0, tk.END)
    entry_original.delete(0, tk.END)
    entry_nuevas.delete(0, tk.END)
    limpiar_filas_ingredientes()
    resultado.delete(*resultado.get_children())

    if seleccion == "Personalizada (ingresar manualmente)":
        # El usuario ingresará todos los datos por su cuenta
        agregar_ingrediente()
        entry_receta.focus_set()
        return

    # Cargar datos conocidos de la receta predeterminada
    entry_receta.insert(0, seleccion.split(" (")[0])
    entry_original.insert(0, str(receta["personas"]))

    for nom, cant, uni in receta["ingredientes"]:
        agregar_ingrediente(nom, str(cant), uni)

    entry_nuevas.focus_set()


def calcular():
    try:
        personas_original = float(entry_original.get())
        personas_nuevas = float(entry_nuevas.get())

        if personas_original <= 0 or personas_nuevas <= 0:
            messagebox.showerror("Error", "Las personas deben ser mayores que 0")
            return

        factor = personas_nuevas / personas_original

        resultado.delete(*resultado.get_children())

        for nombre, cantidad, unidad in ingredientes:
            nom = nombre.get().strip()

            if nom == "":
                continue

            cant = float(cantidad.get())
            uni = unidad.get()

            nueva = cant * factor

            resultado.insert(
                "",
                "end",
                values=(nom, f"{nueva:.2f}", uni)
            )

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores válidos")


def limpiar():
    entry_receta.delete(0, tk.END)
    entry_original.delete(0, tk.END)
    entry_nuevas.delete(0, tk.END)
    combo_recetas.set("")

    limpiar_filas_ingredientes()
    resultado.delete(*resultado.get_children())

    agregar_ingrediente()


# ========================
# VENTANA PRINCIPAL
# ========================
ventana = tk.Tk()
ventana.title("Calculadora de Recetas")
ventana.geometry("1400x800")
ventana.configure(bg=BG)

# Header
header = tk.Frame(ventana, bg=BG)
header.pack(fill="x", pady=15)

tk.Label(
    header,
    text="🍳 Calculadora de Recetas",
    font=("Segoe UI", 28, "bold"),
    bg=BG,
    fg="#D35400"
).pack()

tk.Label(
    header,
    text="Ajusta recetas usando Matemáticas",
    font=("Segoe UI", 14),
    bg=BG,
    fg=TEXT
).pack()

# Contenedor principal
main = tk.Frame(ventana, bg=BG)
main.pack(fill="both", expand=True, padx=20, pady=10)

# ========================
# PANEL IZQUIERDO
# ========================
panel_izq = tk.Frame(main, bg=CARD, bd=2, relief="groove")
panel_izq.pack(side="left", fill="y", padx=10)

tk.Label(
    panel_izq,
    text="DATOS DE LA RECETA",
    bg=CARD,
    fg="#D35400",
    font=("Segoe UI", 16, "bold")
).pack(pady=20)

# --- Selector de receta predeterminada ---
tk.Label(
    panel_izq,
    text="¿No conoce las cantidades originales?",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "italic"),
    wraplength=220,
    justify="center"
).pack(pady=(0, 3))

tk.Label(panel_izq, text="Elija una receta predeterminada", bg=CARD).pack()
combo_recetas = ttk.Combobox(
    panel_izq,
    values=list(RECETAS_PREDETERMINADAS.keys()),
    width=27,
    state="readonly"
)
combo_recetas.pack(pady=8)
combo_recetas.bind("<<ComboboxSelected>>", cargar_receta_predeterminada)

tk.Frame(panel_izq, bg="#E0E0E0", height=1).pack(fill="x", padx=15, pady=10)

tk.Label(panel_izq, text="Nombre receta", bg=CARD).pack()
entry_receta = tk.Entry(panel_izq, width=25, font=("Segoe UI", 11))
entry_receta.pack(pady=8)

tk.Label(panel_izq, text="Personas originales", bg=CARD).pack()
entry_original = tk.Entry(panel_izq, width=25, font=("Segoe UI", 11))
entry_original.pack(pady=8)

tk.Label(panel_izq, text="Nuevas personas", bg=CARD).pack()
entry_nuevas = tk.Entry(panel_izq, width=25, font=("Segoe UI", 11))
entry_nuevas.pack(pady=8)


tk.Button(
    panel_izq,
    text="Reiniciar",
    command=limpiar,
    bg=ORANGE,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=20
).pack(pady=20)

# ========================
# PANEL CENTRAL
# ========================
panel_centro = tk.Frame(main, bg=CARD, bd=2, relief="groove")
panel_centro.pack(side="left", fill="both", expand=True, padx=10)

tk.Label(
    panel_centro,
    text="INGREDIENTES",
    bg=CARD,
    fg="#D35400",
    font=("Segoe UI", 16, "bold")
).pack(pady=15)

frame_tabla = tk.Frame(panel_centro, bg=CARD)
frame_tabla.pack()

headers = ["Ingrediente", "Cantidad", "Unidad"]
for i, h in enumerate(headers):
    tk.Label(
        frame_tabla,
        text=h,
        width=18,
        bg=ORANGE,
        fg="white",
        font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=i, padx=2, pady=2)

tk.Button(
    panel_centro,
    text="➕ Agregar ingrediente",
    command=agregar_ingrediente,
    bg=ORANGE,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=25
).pack(pady=20)

tk.Button(
    panel_centro,
    text="🧮 CALCULAR RECETA",
    command=calcular,
    bg=GREEN,
    fg="white",
    font=("Segoe UI", 16, "bold"),
    width=25,
    height=2
).pack(pady=20)

# ========================
# PANEL DERECHO
# ========================
panel_der = tk.Frame(main, bg=CARD, bd=2, relief="groove")
panel_der.pack(side="right", fill="y", padx=10)

tk.Label(
    panel_der,
    text="RESULTADOS",
    bg=CARD,
    fg=GREEN,
    font=("Segoe UI", 16, "bold")
).pack(pady=15)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    rowheight=35,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

resultado = ttk.Treeview(
    panel_der,
    columns=("ingrediente", "cantidad", "unidad"),
    show="headings",
    height=16
)

resultado.heading("ingrediente", text="Ingrediente")
resultado.heading("cantidad", text="Cantidad")
resultado.heading("unidad", text="Unidad")

resultado.column("ingrediente", width=180)
resultado.column("cantidad", width=120)
resultado.column("unidad", width=100)

resultado.pack(padx=10, pady=10)

agregar_ingrediente()

ventana.mainloop()
