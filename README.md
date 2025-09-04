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


