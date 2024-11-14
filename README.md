# Repositorio del proyecto de PGPI del grupo G3.1

## Instrucciones de instalación y desarrollo del proyecto

- [Repositorio del proyecto de PGPI del grupo G3.1](#repositorio-del-proyecto-de-pgpi-del-grupo-g31)
  - [Instrucciones de instalación y desarrollo del proyecto](#instrucciones-de-instalación-y-desarrollo-del-proyecto)
    - [Requsitos previos](#requsitos-previos)
    - [1. Clonar el repositorio en VSCode](#1-clonar-el-repositorio-en-vscode)
    - [2. Crear la base de datos](#2-crear-la-base-de-datos)
    - [3. Crear entorno virtual, instalar requisitos, ejecutar](#3-crear-entorno-virtual-instalar-requisitos-ejecutar)
    - [4. Desarrollo de funcionalidades en el código](#4-desarrollo-de-funcionalidades-en-el-código)
    - [5. Metodología para realizar cambios](#5-metodología-para-realizar-cambios)
    - [6. Recarga de BBDD](#6-recarga-de-bbdd)


---

### Requsitos previos

- Postgresql 17 (BBDD)
- Anaconda (Entornos virtuales)
- Visual Studio Code (IDE)
- Dbeaver (Gestión de BBDD) (Recomendado)

### 1. Clonar el repositorio en VSCode

### 2. Crear la base de datos
Entrar en la línea de comandos de postgresql:

`cd "C:\Program Files\PostgreSQL\17\bin"`
`psql -U postgres`

Crear la base de datos y usuario. Introducir los siguientes comandos:

```
CREATE DATABASE safeport;
CREATE USER safeport_user WITH PASSWORD 'safeport_password';
GRANT ALL PRIVILEGES ON DATABASE safeport TO safeport_user;
\c safeport;
GRANT USAGE ON SCHEMA public TO safeport_user;
GRANT CREATE ON SCHEMA public TO safeport_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO safeport_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO safeport_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO safeport_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO safeport_user;
\q
```

Para verificar la base de datos: entrar en DBeaver, crear nueva conexión PostgreSQL y completar con los datos:
```
host: localhost
database: safeport
username: safeport_user
password: safeport_password
```

Comprobar que aparece la base de datos

### 3. Crear entorno virtual, instalar requisitos, ejecutar
Usando anaconda se aisla el entorno de desarrollo y gestionan dependencias.

Abrir anaconda prompt y ejecutar:

`conda create -n safeport python=3.12`

En vscode, CTRL+Shift+P y seleccionar: “Python: Select Interpreter”
Elegir el entorno safeport
Abrir una nueva terminal cmd en el workspace y comprobar que usa safeport. Ejecutar:
`pip install -r requirements.txt`
`python manage.py migrate`
`python manage.py runserver`

Al navegar a `http://127.0.0.1:8000/`, se podrá comprobar que se ha iniciado el proyecto correctamente.

### 4. Desarrollo de funcionalidades en el código

Para crear un nuevo módulo, ejecutar `python manage.py startapp <nuevo_modulo>`.
En cada módulo, se tienen los siguientes archivos:
- `models.py`: Contiene las entidades. Cuando se creen nuevas o se realicen modificaciones, se deberá ejecutar `python manage.py makemigrations` para crear el archivo de migraciones, seguido de `python manage.py migrate` para aplicarlas.
- `urls.py`: Contiene las rutas del módulo.
- `views.py`: Contiene los métodos usados por las rutas.
- `/utils`: Carpeta donde se almacenarán funciones de utilidad para los métodos.
- `/static`: Carpeta donde se almacenan los elementos estáticos para renderizar la aplicación web.
- `/static/templates`: Carpeta que contiene las plantillas HTML de las vistas de los métodos.
- `/static/js`: Funciones de javascript para las vistas.
- `tests.py`: Pruebas unitarias.

### 5. Metodología para realizar cambios

Se tiene una rama principal, que requiere la aprobación del administrador para ser modificada. Para el desarrollo, se deberán crear ramas a partir de `develop`, y una vez finalizado el desarrollo de una funcionalidad, crear una `pull request`.

### 6. Recarga de BBDD
Comando para reconstruir la base de datos y repoblarla:

`python manage.py reset_and_populate_db`