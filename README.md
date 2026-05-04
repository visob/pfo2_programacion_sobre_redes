# PFO2 - Sistema de gestión de tareas - Victoria Sobral

API REST con Flask y SQLite. Permite registrar usuarios, iniciar sesión y acceder a un panel de tareas. Las contraseñas se guardan hasheadas con bcrypt.

---

## Requisitos

- Python 3.8 o superior
- pip

---

## Instalación

Clonar el repositorio y entrar a la carpeta:

```bash
git clone https://github.com/visob/pfo2_programacion_sobre_redes
cd pfo2
```

Instalar las dependencias:

```bash
pip install flask bcrypt
```

---

## Cómo correrlo

```bash
python servidor.py
```

El servidor queda corriendo en `http://127.0.0.1:5000`. El archivo `database.db` se crea solo la primera vez.

---

## Endpoints

### POST /registro

Crea un usuario nuevo.

**Body:**
```json
{
  "usuario": "marcela",
  "contraseña": "pass123"
}
```

**Respuestas:**
- `201` — usuario registrado
- `400` — faltan datos
- `409` — ese usuario ya existe

---

### POST /login

Inicia sesión. Si las credenciales son correctas guarda la sesión y habilita el acceso a `/tareas`.

**Body:**
```json
{
  "usuario": "marcela",
  "contraseña": "pass123"
}
```

**Respuestas:**
- `200` — bienvenido
- `400` — faltan datos
- `401` — usuario o contraseña incorrectos

---

### GET /tareas

Muestra el panel de bienvenida. Solo accesible si el usuario inició sesión.

Abrir en el navegador: `http://127.0.0.1:5000/tareas`

**Respuestas:**
- `200` — devuelve el HTML del panel
- `401` — tenes que iniciar sesión primero

---

## Preguntas conceptuales

**¿Por qué hashear contraseñas?**

Si la contraseña se guarda tal cual en la base de datos y alguien accede a ella, tiene las contraseñas de todos en texto plano. Con bcrypt se guarda un hash irreversible, o sea aunque roben el archivo `.db` no pueden saber la contraseña original. Además bcrypt agrega un "salt" automático, lo que hace que dos usuarios con la misma contraseña tengan hashes distintos y evita ataques por tablas de hash precomputadas.

**Ventajas de SQLite en este proyecto**

No hace falta instalar ni configurar nada extra. Toda la base de datos queda en un solo archivo `.db` que se crea automáticamente. Python ya incluye el módulo `sqlite3` en su librería estándar, así que no hay dependencias adicionales. Para un proyecto de esta escala es más que suficiente.

---

## Estructura del proyecto

```
pfo2/
├── servidor.py   
├── database.db    # se genera automáticamente
└── README.md      
```
