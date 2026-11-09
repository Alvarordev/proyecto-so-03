# 🎓 Sistema de Reservas Académicas de Laboratorio

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Base%20de%20datos-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Contenedores-2496ED?logo=docker&logoColor=white)

Aplicación web desarrollada como proyecto académico de **Sistemas Operativos** para registrar y administrar las reservas de laboratorios utilizados en cursos como Programación, Redes, Sistemas Operativos y Ciberseguridad.

El proyecto permite explorar el funcionamiento de una aplicación **monolítica**, su relación con los procesos, servicios y el almacenamiento local del sistema operativo, y su posterior despliegue mediante **Docker**.

## ✨ Funcionalidades

- **Registrar reservas** indicando curso, responsable y cantidad de horas.
- **Visualizar reservas** en un listado ordenado por los registros más recientes.
- **Editar reservas** existentes.
- **Eliminar reservas**.
- **Consultar un resumen** con el número de registros y el total de horas reservadas.
- **Guardar información en SQLite**.
- **Comprobar el estado del servicio** mediante el endpoint `/health`.
- **Ejecutar la aplicación localmente o en un contenedor Docker**.

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
| --- | --- |
| Python | Lógica de la aplicación |
| Flask 3.0.3 | Servidor web y rutas HTTP |
| SQLite | Persistencia local de los registros |
| HTML / CSS | Interfaz web mediante plantillas y archivos estáticos |
| Docker | Empaquetado y ejecución en contenedores |

## 📁 Estructura del proyecto

```text
proyecto-so-03/
├── app.py             # Aplicación Flask, rutas y operaciones CRUD
├── config.py          # Configuración del escenario, campos, puerto y datos iniciales
├── requirements.txt   # Dependencias de Python
├── Dockerfile         # Definición de la imagen Docker
├── templates/         # Plantillas HTML
├── static/            # Archivos estáticos de la interfaz
└── README.md          # Documentación del proyecto
```

La base de datos `reservas.db` se crea al iniciar la aplicación, si todavía no existe. El proyecto incluye tres registros de ejemplo para la primera ejecución con una tabla vacía.

## 🚀 Instalación y ejecución local

### Requisitos previos

- Python 3 instalado.
- `pip` disponible.
- Git (opcional, para clonar el repositorio).

### 1. Clonar el repositorio

```bash
git clone https://github.com/Alvarordev/proyecto-so-03.git
cd proyecto-so-03
```

### 2. Crear un entorno virtual (recomendado)

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Iniciar el servidor

```bash
python app.py
```

Abre la aplicación en tu navegador:

**http://localhost:5003**

> El servidor configurado en `app.py` escucha en el puerto **5003**.

## 🐳 Ejecución con Docker

Es necesario tener instalado Docker y disponer del daemon en ejecución.

### 1. Construir la imagen

Desde la carpeta principal del proyecto:

```bash
docker build -t reservas-laboratorio .
```

### 2. Crear e iniciar un contenedor

```bash
docker run --name reservas-laboratorio -p 5003:5003 reservas-laboratorio
```

Visita **http://localhost:5003**.

### 3. Detener o eliminar el contenedor

En otra terminal:

```bash
docker stop reservas-laboratorio
docker rm reservas-laboratorio
```

### 💾 Persistencia de datos en Docker

De forma predeterminada, SQLite almacena los datos dentro del sistema de archivos del contenedor. Para conservarlos al eliminar y recrear el contenedor, utiliza un volumen:

```bash
docker volume create reservas-data
docker run --name reservas-laboratorio -p 5003:5003 \
  -e DB_PATH=/data/reservas.db \
  -v reservas-data:/data \
  reservas-laboratorio
```

> **Nota:** Elimina primero cualquier contenedor anterior con el mismo nombre. La variable de entorno `DB_PATH` permite elegir dónde guardar el archivo SQLite.

## 🌐 Rutas principales

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/` | Muestra las reservas y el resumen general |
| `POST` | `/crear` | Crea una nueva reserva |
| `GET` | `/editar/<item_id>` | Carga una reserva en el formulario de edición |
| `POST` | `/actualizar/<item_id>` | Actualiza una reserva |
| `POST` | `/eliminar/<item_id>` | Elimina una reserva |
| `GET` | `/health` | Devuelve información básica del estado del servicio |

Para comprobar que la aplicación responde:

```bash
curl http://localhost:5003/health
```

## 🧠 Relación con Sistemas Operativos

Este proyecto permite estudiar los siguientes aspectos:

1. **Procesos y servicios:** Flask se ejecuta como un proceso que atiende solicitudes HTTP.
2. **Puertos y redes:** La aplicación escucha en el puerto `5003`, que debe estar correctamente configurado y publicado cuando se utiliza Docker.
3. **Almacenamiento:** SQLite guarda los registros en un archivo local; por ello es importante gestionar su ubicación y los respaldos.
4. **Despliegue monolítico:** La interfaz web, la lógica de negocio y la base de datos funcionan en un mismo entorno de ejecución.
5. **Contenedorización:** Docker permite empaquetar la aplicación y sus dependencias para reproducir el entorno en otros equipos.
6. **Persistencia:** Los volúmenes de Docker ayudan a mantener la base de datos fuera del ciclo de vida de un contenedor específico.

### Comparación de despliegues

| Aspecto | Ejecución local | Ejecución con Docker |
| --- | --- | --- |
| Dependencias | Se instalan en el sistema o entorno virtual | Se incluyen en la imagen |
| Ejecución | Proceso de Python en el equipo | Proceso dentro de un contenedor |
| Configuración | Depende del entorno local | Definida parcialmente en el `Dockerfile` |
| Datos SQLite | Archivo en el sistema local | Archivo en el contenedor o en un volumen |
| Portabilidad | Requiere preparar el entorno | Facilita reproducir el despliegue |

## ⚙️ Configuración

Los parámetros principales se encuentran en `config.py`:

- **Título:** Reservas académicas de laboratorio.
- **Puerto:** `5003`.
- **Base de datos por defecto:** `reservas.db`.
- **Campos:** `curso`, `responsable` y `horas`.
- **Datos de ejemplo:** reservas iniciales de Sistemas Operativos, Redes y DevOps.

También es posible cambiar la ruta de la base de datos mediante la variable de entorno `DB_PATH`.

## ⚠️ Consideraciones

Este proyecto está orientado al **aprendizaje y la demostración académica**. Antes de utilizarlo en producción, sería recomendable incorporar autenticación, validaciones adicionales, gestión segura de claves, copias de seguridad y un servidor WSGI adecuado.

## 👨‍💻 Autor

Desarrollado por [Alvarordev](https://github.com/Alvarordev).

Repositorio: [github.com/Alvarordev/proyecto-so-03](https://github.com/Alvarordev/proyecto-so-03)
