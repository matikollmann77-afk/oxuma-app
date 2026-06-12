"""
init_precios.py — Inicializa oxuma.db con precios individuales de cada producto.
Correr UNA SOLA VEZ (o cuando quieras resetear los precios al valor de lista).
"""

import os, json, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, "oxuma.db")
JSON = os.path.join(BASE, "productos_raw.json")

# ── Precios de costo reales (precio mayorista/minorista que paga Oxuma)
# Fuente: listas de proveedores (MINIMO3 / precio mayor / X3)
# Los que no están aquí se calculan con margen 30% por defecto.
COSTOS = {
    # ── LÁMPARAS (precio MINIMO3 del PDF Lamparas JUNIO) ──────────────────
    "LAMPARA AFRICANA":          8330,
    "LAMPARA AURORA":            7910,
    "LAMPARA CLEMENTINE":        7761,
    "LAMPARA CUENTO RÚSTICO":    11208,
    "LAMPARA HEXA FACETADA":     12370,
    "LAMPARA NIDITO LOVE":       5643,
    "LAMPARA PIEDRA AROMA":      27289,
    "Pirámide":                   9190,
    "Pirámide Lux":              17271,
    "Vasito de Luz":             12715,
    "Vasito Conico":             13027,
    "Vasito Ro":                  7848,
    "Zapallito":                  7695,
    "Ollita de Sal":              7848,
    "Ollita con tapa":            7657,
    "Jarrón Japones":            12541,
    "Jarrón Japonés Mini":        7810,
    "Jarrón con tapa":           13100,
    "Jarrito de Sal":             7528,
    "Elefantito":                 9680,
    "Esfera Cristal":             7313,
    "Esfera Cristal Grande":     11400,
    "BUDA DURMIENDO":             8904,
    "Cuenco Amazonas":            8024,
    "MANOS ABUNDANCIA":           9350,
    "Mano Ancestral":             7698,
    "OM OM":                      8415,
    "Ostra":                      7200,
    "Ostra Abierta":              8181,
    "Hojita":                     9767,
    "Gatito Luz":                12153,
    "Gotita Calada":             13079,
    "Gotita Flor":               12153,
    "Patito":                    11703,
    "Pachamama":                 17824,
    "Mulata":                    14262,
    "Nenitas":                   14712,
    "Cazuela de Sal":            13092,
    "Media Esfera Chica":        12307,
    "Media Esfera Mediana":      15540,
    "Media Esfera Grande":       17594,
    "PIEDRA GRANDE":             15579,
    "Piedra Mediana":            19108,
    "Piedra Chica":              11250,
    "Torre Inclinada":           12374,
    "Lámpara Africana Pintada":  14421,
    "Lámpara Loto XL":           18040,
    "Lechuza con flor":          14422,
    "Elefante Copa Pintada":     19137,
    "Elefante Prosperidad":      13849,
    "Elefante Vasija":            7683,
    "Hijo del Sol Chico":        12727,
    "Hijo del Sol Mediana":      16530,
    "Hijo del Sol Grande":       18424,
    # ── SAPHIRUS (precio 3-11u del PDF) ──────────────────────────────────
    # Aproximado: ~75% del PUBLICO (margen ~33%)
    # (los valores exactos 3-11u no estaban en el resumen, usamos 75%)
    # ── HUMIDIFICADORES (precio X2 si hubiera, sino 80% del X1) ──────────
}

MARGEN_DEFAULT = 30.0   # % que Oxuma aplica cuando no conocemos el costo exacto

def porcentaje_margen(costo, venta):
    if costo and costo > 0:
        return round((venta - costo) / costo * 100, 2)
    return MARGEN_DEFAULT

conn = sqlite3.connect(DB)
c = conn.cursor()

# ── Crear tablas ──────────────────────────────────────────────────────────────
c.executescript("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        marca TEXT,
        precio_costo REAL DEFAULT 0,
        margen REAL DEFAULT 30,
        precio_venta REAL DEFAULT 0,
        stock INTEGER DEFAULT 0,
        activo INTEGER DEFAULT 1,
        updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cuit TEXT,
        email TEXT,
        telefono TEXT,
        direccion TEXT,
        tipo TEXT DEFAULT 'mayorista',
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT,
        total REAL DEFAULT 0,
        estado TEXT DEFAULT 'pendiente',
        notas TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );
    CREATE TABLE IF NOT EXISTS pedido_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER DEFAULT 1,
        precio_unitario REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
    CREATE TABLE IF NOT EXISTS historial_precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        precio_anterior REAL,
        precio_nuevo REAL,
        motivo TEXT,
        fecha TEXT,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
""")

# ── Cargar productos ──────────────────────────────────────────────────────────
existing = c.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
if existing > 0:
    print(f"⚠️  La tabla ya tiene {existing} productos.")
    resp = input("¿Querés BORRAR y recargar desde cero? (s/n): ").strip().lower()
    if resp == "s":
        c.execute("DELETE FROM productos")
        conn.commit()
        print("   Tabla limpiada.")
    else:
        print("   No se hizo nada. Saliendo.")
        conn.close()
        exit()

with open(JSON, "r", encoding="utf-8") as f:
    raw = json.load(f)

now = datetime.now().isoformat()
cargados = 0
sin_precio = 0

for p in raw:
    nombre = p.get("nombre", "").strip()
    if not nombre:
        continue

    precio_venta = float(p.get("precio", 0) or 0)
    if precio_venta == 0:
        sin_precio += 1
        continue

    # Buscar costo real; si no hay, back-calculate con margen default
    costo_real = COSTOS.get(nombre)
    if costo_real:
        precio_costo = float(costo_real)
        margen = porcentaje_margen(precio_costo, precio_venta)
    else:
        # Estimamos costo = venta / (1 + margen_default/100)
        precio_costo = round(precio_venta / (1 + MARGEN_DEFAULT / 100), 2)
        margen = MARGEN_DEFAULT

    c.execute("""
        INSERT INTO productos (nombre, categoria, marca, precio_costo, margen, precio_venta, stock, activo, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, 1, ?)
    """, (nombre, p.get("categoria", ""), p.get("marca", ""),
          precio_costo, margen, precio_venta, now))
    cargados += 1

conn.commit()
conn.close()

print(f"\n✅  Listo! Se cargaron {cargados} productos con precios individuales.")
print(f"   ({sin_precio} sin precio ignorados)")
print(f"\n   Ahora iniciá la app con INICIAR APP.bat")
