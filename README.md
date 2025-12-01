# 📁 Aplicación Administrador de Archivos

**FilePilot** es una aplicación de administración de archivos escrita en **Python** que migró exitosamente de una app de escritorio con `tkinter` a una solución web moderna basada en **Flask**. Permite navegar, cargar, descargar y organizar archivos desde el navegador, con una interfaz intuitiva y preparada para despliegue local o en la nube (como Vercel).

---

## 🖼️ Vistas Previas

| Navegador de Archivos | Página Principal | Resultados de Búsqueda |
|------------------------|------------------|-------------------------|
| ![](https://github.com/frontenddeveloper2025dev/FilePilot/blob/main/file%20manager%20%201.png) | ![](https://github.com/frontenddeveloper2025dev/FilePilot/blob/main/file%20manager%20.png) | ![](https://github.com/frontenddeveloper2025dev/FilePilot/blob/main/file%20manager%20%202.png) |

---

## ⚙️ Tecnologías Utilizadas

- **Python 3.x**
- **Flask** – Framework web ligero
- **Jinja2** – Motor de plantillas HTML
- **SQLite** – Base de datos para registro de acciones (opcional)
- **pathlib, os, shutil** – Manejo del sistema de archivos
- Compatible con despliegue local, serverless (Vercel) y producción (Gunicorn)

---

## 🚀 Funcionalidades Principales

- 📂 Navegación de carpetas y archivos en tiempo real
- ⬆️ Carga de archivos desde la interfaz
- ➕ Creación de carpetas y estructura personalizada
- 🔍 Búsqueda avanzada con filtros
- 🧠 Detección de tipos de archivo y metadatos
- 🔒 Seguridad integrada (validación de rutas, control de caché, prevención de comandos maliciosos)
- 💡 Interfaz completamente en español

---

## 🧱 Arquitectura del Proyecto

### 🔹 Framework Web (Flask)

- `web_server.py`: punto de entrada, manejo de rutas y renderizado
- Plantillas en Jinja2:
  - `base.html`: estructura global
  - `index.html`: vista principal de archivos
  - `search.html`: resultados filtrados
  - `error.html`: manejo de errores

### 🔹 Diseño Modular

- **FileOperations**: operaciones de archivos (navegar, copiar, eliminar, renombrar, etc.)
- **Utils**: utilidades de formato (tamaños legibles, fechas, validación)
- **Web Server**: renderizado de páginas y controladores HTTP

### 🔹 Seguridad

- Validación y sanitización de rutas
- Prevención de traversal (`../`) y accesos no autorizados
- Cabeceras para evitar almacenamiento en caché de contenido sensible
- Control de excepciones en operaciones críticas

---

## 📂 Almacenamiento y Compatibilidad

- 📦 Compatible con Windows, Linux y macOS
- 🗃️ Soporte local para SQLite si se desea llevar un log de eventos
- 🧠 Manejo de estado mediante variables globales (directorio actual, historial)

---

## 🌐 Despliegue

### 1. 🔧 Desarrollo local

```bash
python web_server.py


2. ☁️ Despliegue Serverless (Vercel)

Incluye archivo vercel.json para compatibilidad:

{
  "builds": [{ "src": "web_server.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "web_server.py" }]
}

3. 🖥️ Producción tradicional con Gunicorn
gunicorn web_server:app

📁 Estructura del Proyecto
FilePilot/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   └── error.html
├── static/
│   └── styles.css
├── utils.py
├── file_operations.py
├── web_server.py
├── vercel.json
└── README.md

👩‍💻 Autora

Desarrollado por frontenddeveloper2025dev, como proyecto evolutivo que transforma una app de escritorio en una solución web ligera, segura y preparada para la nube.
