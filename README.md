<a id="readme-top"></a>

<div align="center">

  <img src="src/assets/logo.png" alt="Dagent Logo" width="180" height="180" />

  # Dagent

  **Sistema ágil y ligero para la gestión de clientes y ventas**

  [![Status](https://img.shields.io/badge/status-in--development-yellow?style=for-the-badge)](https://github.com/wh1te-fox/Dagent)
  [![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Flet](https://img.shields.io/badge/Flet-UI-FF4136?style=for-the-badge&logo=flutter&logoColor=white)](https://flet.dev/)
  [![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](LICENSE)

  <p align="center">
    <a href="#-características">Características</a> •
    <a href="#-tecnologías">Tecnologías</a> •
    <a href="#-instalación">Instalación</a> •
    <a href="#-novedades">Novedades</a>
  </p>

</div>

---

> **Espacio de Experimentación:** Este repositorio está dedicado a la exploración, validación y optimización de tecnologías. Si tienes propuestas de mejora o nuevas funcionalidades, ¡las contribuciones son bienvenidas!

---

## Características

-  **Gestión de Clientes:** Registro, actualización y búsqueda centralizada de clientes.
-  **Control de Ventas:** Registro de transacciones y catálogo de productos.
-  **Interfaz Moderna:** Experiencia multiplataforma fluida construida sobre Flet.
-  **Almacenamiento Local:** Integración ligera y veloz con SQLite.

---

##  Tecnologías

| Tecnología | Descripción |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Lenguaje base (v3.12+) |
| ![Flet](https://img.shields.io/badge/Flet-FF4136?style=flat-square&logo=flutter&logoColor=white) | Framework para interfaz gráfica (UI) |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Motor de base de datos relacional |

---

## Instalación

Sigue estos pasos para clonar y ejecutar el proyecto localmente:

### 1. Clonar el repositorio
```bash
git clone git@github.com:wh1te-fox/Dagent.git
cd Dagent

```

### 2. Configurar el entorno virtual

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

### 4. Ejecutar la aplicación

```bash
python src/page.py

```

---

##  Novedades (Rama Activa)

Las últimas actualizaciones integradas en la nueva rama incluyen:

*  **Consultas SQL optimizadas:** Refactorización en los módulos de búsqueda y productos (`Code/SQL/`).
*  **Mejoras en la interfaz:** Flujo de entrada de datos y actualización de clientes simplificados.
*  **Refactorización de código:** Modularización limpia de controladores y compatibilidad asegurada con Python 3.12+.

---

##  Licencia

Distribuido bajo la licencia **GPL-3.0**. Consulta el archivo [`LICENSE`](https://www.google.com/search?q=LICENSE) para obtener más información.
