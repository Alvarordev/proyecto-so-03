import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from config import TITLE, EMOJI, SCENARIO, PORT, DB_NAME, FIELDS, SEED, SUMMARY_COL, SUMMARY_LABEL

app = Flask(__name__)
app.secret_key = "demo-key"

def db_path():
    return os.getenv("DB_PATH", DB_NAME)

def conn():
    c = sqlite3.connect(db_path())
    c.row_factory = sqlite3.Row
    return c

def init_db():
    path = db_path()
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    cols = ", ".join([f"{name} {'REAL' if typ == 'number' else 'TEXT'} NOT NULL" for name, label, typ in FIELDS])
    c = conn()
    c.execute(f"CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})")
    total = c.execute("SELECT COUNT(*) AS total FROM items").fetchone()["total"]
    if total == 0:
        names = ", ".join([f[0] for f in FIELDS])
        marks = ", ".join(["?"] * len(FIELDS))
        c.executemany(f"INSERT INTO items ({names}) VALUES ({marks})", SEED)
    c.commit()
    c.close()

def form_values():
    values = []
    for name, label, typ in FIELDS:
        value = request.form.get(name, "")
        values.append(float(value or 0) if typ == "number" else value.strip())
    return values

@app.route("/")
def index():
    c = conn()
    items = c.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    resumen = c.execute(f"SELECT COUNT(*) registros, COALESCE(SUM({SUMMARY_COL}),0) total FROM items").fetchone()
    c.close()
    return render_template("index.html", title=TITLE, emoji=EMOJI, scenario=SCENARIO, fields=FIELDS, items=items, resumen=resumen, summary_label=SUMMARY_LABEL, edit_item=None)

@app.route("/crear", methods=["POST"])
def crear():
    names = ", ".join([f[0] for f in FIELDS])
    marks = ", ".join(["?"] * len(FIELDS))
    c = conn()
    c.execute(f"INSERT INTO items ({names}) VALUES ({marks})", form_values())
    c.commit()
    c.close()
    flash("Registro creado correctamente.")
    return redirect(url_for("index"))

@app.route("/editar/<int:item_id>")
def editar(item_id):
    c = conn()
    items = c.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    edit_item = c.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    resumen = c.execute(f"SELECT COUNT(*) registros, COALESCE(SUM({SUMMARY_COL}),0) total FROM items").fetchone()
    c.close()
    return render_template("index.html", title=TITLE, emoji=EMOJI, scenario=SCENARIO, fields=FIELDS, items=items, resumen=resumen, summary_label=SUMMARY_LABEL, edit_item=edit_item)

@app.route("/actualizar/<int:item_id>", methods=["POST"])
def actualizar(item_id):
    set_clause = ", ".join([f"{name}=?" for name, label, typ in FIELDS])
    c = conn()
    c.execute(f"UPDATE items SET {set_clause} WHERE id=?", form_values() + [item_id])
    c.commit()
    c.close()
    flash("Registro actualizado correctamente.")
    return redirect(url_for("index"))

@app.route("/eliminar/<int:item_id>", methods=["POST"])
def eliminar(item_id):
    c = conn()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    c.commit()
    c.close()
    flash("Registro eliminado correctamente.")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok", "app": TITLE, "database": "SQLite", "port": PORT}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)
