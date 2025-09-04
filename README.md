# Aplicación Administrador de Archivos

## Resumen
Esta es una aplicación de administrador de archivos basada en Python que ha evolucionado de una aplicación de escritorio con tkinter a un sistema de gestión de archivos basado en la web. La aplicación ofrece una interfaz accesible desde el navegador para operaciones comunes del sistema de archivos, incluyendo navegación, carga y descarga de archivos, creación de directorios y funcionalidad de búsqueda. Está diseñada para su despliegue en plataformas serverless como Vercel e incluye capacidades tanto para desarrollo local como configuraciones para despliegue en la nube.

## Preferencias del Usuario
- **Estilo de comunicación preferido:** Lenguaje simple y cotidiano.

## Arquitectura del Sistema

### Arquitectura del Framework Web
La aplicación utiliza Flask como framework web principal, proporcionando una base ligera y flexible para la interfaz de gestión de archivos. El servidor web (`web_server.py`) maneja todo el enrutamiento HTTP y sirve plantillas HTML mediante el motor de plantillas Jinja2.

### Patrón de Diseño Modular
La base de código sigue una clara separación de responsabilidades con tres módulos principales:

- **Módulo FileOperations:** Encapsula todas las operaciones del sistema de archivos, incluyendo recorrido de directorios, detección de tipos de archivo y extracción de metadatos.  
- **Módulo Utils:** Proporciona funciones utilitarias para formateo de tamaños de archivo, manejo de fechas y validación de nombres de archivo.  
- **Módulo Web Server:** Gestiona las solicitudes HTTP, renderizado de plantillas y puntos finales de la API.

### Arquitectura de Interfaz Basada en Plantillas
La interfaz de usuario está construida usando renderizado del lado servidor con plantillas Jinja2:

- **Plantilla Base:** Proporciona un diseño, estilo y estructura de navegación consistentes.  
- **Plantilla Index:** Interfaz principal del explorador de archivos con capacidades de carga y creación de carpetas.  
- **Plantilla Search:** Página dedicada a resultados de búsqueda con opciones de filtrado.  
- **Plantilla Error:** Manejo estandarizado de errores y retroalimentación al usuario.

### Integración con el Sistema de Archivos
Las operaciones de archivos utilizan la biblioteca estándar de Python (`pathlib`, `os`, `shutil`) para compatibilidad multiplataforma. La aplicación mantiene el estado de la sesión mediante variables globales que rastrean el directorio actual e implementa manejo seguro de archivos con validación de rutas.

## Características de Seguridad
La aplicación incluye varias medidas de seguridad:

- Validación de rutas para prevenir ataques de traversal de directorios.  
- Manejo seguro de archivos con sanitización adecuada de entradas.  
- Encabezados de control de caché para evitar almacenamiento en caché de datos sensibles en el navegador.  
- Prevención de inyección de comandos en operaciones de archivos.

## Arquitectura de Despliegue
La aplicación soporta múltiples escenarios de despliegue:

- **Desarrollo Local:** Ejecución directa del servidor de desarrollo Flask.  
- **Serverless en Vercel:** Configurado con `vercel.json` para despliegue serverless.  
- **Producción con Gunicorn:** Soporte para servidor WSGI en entornos de hosting tradicionales.

## Gestión de Estado
La aplicación utiliza gestión de estado del lado servidor con variables globales para rastrear:

- Directorio de trabajo actual.  
- Historial de navegación del usuario.  
- Contexto de operaciones de archivos.

## Estructura de la API
Los endpoints RESTful manejan las operaciones de archivos:

Método

Ruta

Descripción

GET

/

Interfaz principal del explorador de archivos.

POST

/navigate

Navegación de directorios.

GET

/search

Funcionalidad de búsqueda de archivos.

POST

/upload

Manejo de carga de archivos.

POST

/create_folder

Creación de directorios.

GET

/download/<filename>

Descarga de archivos.

Dependencias Externas
Framework Web de Python
Flask 3.1.2: Framework web principal que provee enrutamiento, templating y manejo de solicitudes.
Jinja2 3.1.6: Motor de plantillas para renderizado HTML del lado servidor.
Werkzeug 3.1.3: Biblioteca WSGI que soporta Flask.
Servidor de Producción
Gunicorn 23.0.0: Servidor HTTP WSGI para despliegues en producción.
Seguridad y Utilidades
MarkupSafe 3.0.2: Manejo de cadenas y prevención de XSS.
Click 8.2.1: Utilidades para interfaces de línea de comandos.
ItsDangerous 2.2.0: Firma criptográfica para manejo seguro de datos.
Blinker 1.9.0: Sistema de manejo de señales/eventos.
Plataforma de Despliegue
Vercel: Plataforma serverless con escalado automático y CDN global.
Python 3.11.9: Entorno de ejecución especificado en runtime.txt.
Operaciones del Sistema de Archivos
La aplicación está construida completamente con módulos de la biblioteca estándar de Python para máxima compatibilidad y mínimas dependencias externas:

pathlib para manejo moderno de rutas.
os y shutil para operaciones del sistema de archivos.
platform para detección de compatibilidad multiplataforma.
