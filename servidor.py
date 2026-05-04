from flask import Flask, request, jsonify, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_123"


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "faltan datos"}), 400

    usuario = datos["usuario"]
    contrasena = datos["contraseña"]

    hash_contra = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
            (usuario, hash_contra.decode("utf-8"))
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "usuario registrado"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "ese usuario ya existe"}), 409


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({"error": "faltan datos"}), 400

    usuario = datos["usuario"]
    contrasena = datos["contraseña"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    fila = cursor.fetchone()
    conn.close()

    if fila is None:
        return jsonify({"error": "usuario o contraseña incorrectos"}), 401

    if bcrypt.checkpw(contrasena.encode("utf-8"), fila[0].encode("utf-8")):
        session["usuario"] = usuario
        return jsonify({"mensaje": f"bienvenido {usuario}"}), 200
    else:
        return jsonify({"error": "usuario o contraseña incorrectos"}), 401


@app.route("/tareas", methods=["GET"])
def tareas():
    if "usuario" not in session:
        return jsonify({"error": "tenes que iniciar sesion primero"}), 401

    usuario = session.get("usuario")
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tareas</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f0e8;
            min-height: 100vh;
        }}
        .main {{
            max-width: 900px;
            margin: 0 auto;
            padding: 48px 40px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 32px;
        }}
        .greeting h1 {{
            font-size: 30px;
            font-weight: 700;
            color: #1a1a1a;
        }}
        .greeting p {{
            font-size: 14px;
            color: #999;
            margin-top: 6px;
        }}
        .cards {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 28px;
        }}
        .card {{
            border-radius: 16px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }}
        .card-yellow {{ background: #e8df4a; }}
        .card-pink   {{ background: #f0a8c0; }}
        .card-green  {{ background: #b8cc6e; }}
        .card-label {{
            font-size: 12px;
            font-weight: 600;
            color: #1a1a1a;
            opacity: 0.6;
            margin-bottom: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .card-value {{
            font-size: 44px;
            font-weight: 700;
            color: #1a1a1a;
            line-height: 1;
        }}
        .card-sub {{
            font-size: 12px;
            color: #1a1a1a;
            opacity: 0.55;
            margin-top: 8px;
        }}
        .card-circle {{
            position: absolute;
            right: -14px;
            bottom: -14px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: rgba(0,0,0,0.07);
        }}
        .section-title {{
            font-size: 12px;
            font-weight: 600;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }}
        .endpoints {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
        }}
        .endpoint-row {{
            display: flex;
            align-items: center;
            padding: 16px 24px;
            border-bottom: 1px solid #f5f0e8;
            gap: 16px;
        }}
        .endpoint-row:last-child {{ border-bottom: none; }}
        .method {{
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            width: 52px;
            text-align: center;
        }}
        .post {{ background: #e8df4a; color: #1a1a1a; }}
        .get  {{ background: #b8cc6e; color: #1a1a1a; }}
        .endpoint-path {{
            font-family: monospace;
            font-size: 14px;
            color: #1a1a1a;
        }}
        .endpoint-desc {{
            font-size: 13px;
            color: #bbb;
            margin-left: auto;
        }}
    </style>
</head>
<body>

<main class="main">
    <div class="header">
        <div class="greeting">
            <h1>Buen dia, {usuario}</h1>
            <p>Sistema de gestion de tareas activo.</p>
        </div>
    </div>

    <div class="cards">
        <div class="card card-yellow">
            <div class="card-label">Endpoints activos</div>
            <div class="card-value">3</div>
            <div class="card-sub">registro · login · tareas</div>
            <div class="card-circle"></div>
        </div>
        <div class="card card-pink">
            <div class="card-label">Base de datos</div>
            <div class="card-value">✓</div>
            <div class="card-sub">SQLite conectado</div>
            <div class="card-circle"></div>
        </div>
        <div class="card card-green">
            <div class="card-label">Seguridad</div>
            <div class="card-value">✓</div>
            <div class="card-sub">bcrypt activo</div>
            <div class="card-circle"></div>
        </div>
    </div>

    <div class="section-title">Endpoints disponibles</div>
    <div class="endpoints">
        <div class="endpoint-row">
            <span class="method post">POST</span>
            <span class="endpoint-path">/registro</span>
            <span class="endpoint-desc">Crear un usuario nuevo</span>
        </div>
        <div class="endpoint-row">
            <span class="method post">POST</span>
            <span class="endpoint-path">/login</span>
            <span class="endpoint-desc">Iniciar sesion</span>
        </div>
        <div class="endpoint-row">
            <span class="method get">GET</span>
            <span class="endpoint-path">/tareas</span>
            <span class="endpoint-desc">Esta pagina</span>
        </div>
    </div>
</main>

</body>
</html>"""
    return html


if __name__ == "__main__":
    init_db()
    app.run(debug=True)