# 🛒 Tienda API

REST API para gestión de una tienda online, desarrollada con **Flask** y **SQLite**. Permite administrar usuarios, productos y pedidos con autenticación JWT y control de roles.

---

## 🚀 Tecnologías

- **Python** + **Flask**
- **SQLite** (base de datos)
- **Flask-JWT-Extended** (autenticación)
- **Werkzeug** (hash de contraseñas)

---

## 📁 Estructura del proyecto

```
├── run.py
├── requirements.txt
├── .env
└── app/
    ├── __init__.py
    ├── database/
    │   └── db.py
    ├── routes/
    │   ├── usuario_routes.py
    │   ├── producto_routes.py
    │   ├── pedidos_routes.py
    │   └── estadisticas_routes.py
    ├── services/
    │   ├── usuario_service.py
    │   ├── producto_service.py
    │   ├── pedidos_service.py
    │   └── estadisticas_service.py
    ├── validators/
    │   ├── usuario_validators.py
    │   ├── producto_validators.py
    │   └── pedidos_validators.py
    └── utils/
        ├── decorators.py
        ├── errors.py
        └── responses.py
```

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Lev-w/sistema-pedidos
cd sistema-pedidos

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo .env
cp .env.example .env
# Editar .env y definir JWT_SECRET_KEY

# 5. Correr el servidor
python run.py
```

---

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints protegidos, primero obtén un token con el endpoint de login e inclúyelo en el header de cada request:

```
Authorization: Bearer <token>
```

---

## 📌 Endpoints

### Usuarios `/usuarios`

| Método | Ruta | Descripción | Auth | Rol |
|--------|------|-------------|------|-----|
| POST | `/usuarios` | Registrar usuario | No | — |
| POST | `/usuarios/login` | Iniciar sesión | No | — |
| GET | `/usuarios/perfil` | Ver perfil propio | Sí | — |
| GET | `/usuarios` | Listar usuarios | Sí | admin |
| GET | `/usuarios/<id>` | Ver usuario por ID | Sí | — |
| DELETE | `/usuarios/<id>` | Eliminar usuario | Sí | admin |

**Registrar usuario** `POST /usuarios`
```json
{
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "password": "mipassword123"
}
```

**Login** `POST /usuarios/login`
```json
{
  "correo": "juan@email.com",
  "password": "mipassword123"
}
```

---

### Productos `/productos`

| Método | Ruta | Descripción | Auth | Rol |
|--------|------|-------------|------|-----|
| POST | `/productos` | Crear producto | Sí | admin |
| GET | `/productos` | Listar productos | Sí | — |
| GET | `/productos/<id>` | Ver producto | Sí | — |
| PUT | `/productos/<id>` | Actualizar producto | Sí | admin |
| DELETE | `/productos/<id>` | Eliminar producto | Sí | admin |

**Crear / actualizar producto**
```json
{
  "nombre": "Zapatillas Nike",
  "descripcion": "Talla 42, color blanco",
  "precio": 89.99,
  "stock": 50
}
```

**Parámetros de listado (query params)**

| Param | Descripción | Default |
|-------|-------------|---------|
| `nombre` | Filtrar por nombre | — |
| `page` | Número de página | 1 |
| `limit` | Resultados por página | 10 |
| `orden` | `precio_asc`, `precio_desc`, `stock_asc`, `stock_desc`, `fecha_asc`, `fecha_desc` | — |

---

### Pedidos `/pedidos`

| Método | Ruta | Descripción | Auth | Rol |
|--------|------|-------------|------|-----|
| POST | `/pedidos` | Crear pedido | Sí | — |
| GET | `/pedidos` | Listar pedidos | Sí | admin |
| GET | `/pedidos/<id>` | Ver pedido | Sí | admin |
| GET | `/pedidos/mis-pedidos` | Ver pedidos propios | Sí | — |
| PUT | `/pedidos/<id>/estado` | Actualizar estado | Sí | admin |
| PUT | `/pedidos/<id>/cancelar` | Cancelar pedido | Sí | — |

**Crear pedido**
```json
{
  "productos": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 3, "cantidad": 1 }
  ]
}
```

**Actualizar estado** `PUT /pedidos/<id>/estado`
```json
{
  "estado": "enviado"
}
```

Estados válidos: `pendiente` → `enviado` → `entregado` / `cancelado`

---

### Estadísticas `/estadisticas`

| Método | Ruta | Descripción | Auth | Rol |
|--------|------|-------------|------|-----|
| GET | `/estadisticas` | Ver estadísticas de ventas | Sí | admin |

**Respuesta**
```json
{
  "ventas_totales": 1540.50,
  "productos_mas_vendidos": [...],
  "usuarios_mas_compradores": [...]
}
```

---

## 📦 Formato de respuestas

**Éxito**
```json
{
  "ok": true,
  "data": { ... },
  "mensaje": "Operación exitosa"
}
```

**Con paginación**
```json
{
  "ok": true,
  "data": [...],
  "mensaje": "...",
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 42,
    "total_pages": 5
  }
}
```

**Error**
```json
{
  "ok": false,
  "error": "Descripción del error"
}
```

---

## 👤 Roles

| Rol | Descripción |
|-----|-------------|
| `cliente` | Rol por defecto al registrarse. Puede ver productos, crear y cancelar sus propios pedidos. |
| `vendedor` | Acceso intermedio (en desarrollo). |
| `admin` | Acceso completo a todos los endpoints. |

---

## 📝 Notas

- Los usuarios y productos se eliminan de forma lógica (`activo = 0`), no se borran de la base de datos.
- Al cancelar un pedido, el stock de los productos se restaura automáticamente.
- Las contraseñas se almacenan con hash usando **Werkzeug**.