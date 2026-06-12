"""
Diagnóstico Jinja2 - ejecutar con: py DIAGNOSTICO.py
"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Python: {sys.version}")
try:
    import jinja2
    print(f"Jinja2:  {jinja2.__version__}")
except ImportError:
    print("ERROR: jinja2 no instalado")
    sys.exit(1)

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

env = Environment(loader=FileSystemLoader("templates"))

templates = [
    "base.html",
    "dashboard.html",
    "catalogo.html",
    "precios.html",
    "clientes.html",
    "pedidos.html",
    "producto_form.html",
]

print("\n--- Verificación de templates ---")
all_ok = True
for name in templates:
    path = os.path.join("templates", name)
    if not os.path.exists(path):
        print(f"  ✗ {name} — ARCHIVO NO EXISTE")
        all_ok = False
        continue
    size = os.path.getsize(path)
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    # Count blocks
    import re
    blocks = re.findall(r'\{%-?\s*block\s+(\w+)', "".join(lines))
    endblocks = re.findall(r'\{%-?\s*endblock', "".join(lines))
    try:
        env.get_template(name)
        print(f"  ✓ {name:30s} {len(lines):4d} líneas  blocks={len(blocks)} endblocks={len(endblocks)}")
        if blocks:
            print(f"    Blocks: {', '.join(blocks)}")
    except TemplateSyntaxError as e:
        print(f"  ✗ {name:30s} línea {e.lineno}: {e.message}")
        # Show surrounding lines
        ctx_start = max(0, e.lineno - 4)
        ctx_end   = min(len(lines), e.lineno + 2)
        for i in range(ctx_start, ctx_end):
            marker = ">>>" if i == e.lineno - 1 else "   "
            print(f"    {marker} {i+1:4d}: {lines[i]}", end="")
        all_ok = False

print("\n" + ("✅ TODOS OK" if all_ok else "❌ HAY ERRORES — ver detalle arriba"))
print("\nPresioná Enter para salir...")
input()
