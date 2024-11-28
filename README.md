# Repositorio del proyecto de PGPI del grupo G3.1

Proyecto desplegado: `https://safeport.onrender.com`

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
    - [7. Docker](#7-docker)
    - [8. Integración con Stripe](#8-integración-con-stripe)
      - [8.1 Stripe para el entorno de desarrollo](#81-stripe-para-el-entorno-de-desarrollo)
      - [8.2 Stripe para la imagen Docker en local](#82-stripe-para-la-imagen-docker-en-local)


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


### 7. Docker
Desde cmd en root en vscode:

`docker-compose build --no-cache`

`docker-compose up`

Accesible en:

`http://localhost:8000/`

### 8. Integración con Stripe

Para el funcionamiento de los pagos en línea, hacen falta las credenciales de Stripe. Estas varían según el entorno de
desarrollo o el de despliegue.

#### 8.1 Stripe para el entorno de desarrollo

Será necesario crearse una cuenta en Stripe `https://stripe.com`. Al registrarse se creará una cuenta de prueba. Esta tendrá todas las funcionalidades para poder probar el correcto funcionamiento de la pasarela de pago, dejando a manos del cliente el que configure su propia página en Stripe con la imagen dada; instrucciones que se detallarán en el siguiente punto.

Desde el dashboard, en Developers -> API Keys, se pueden obtener dos de las claves necesarias. Estas se deben incluir en el env de configuración en el entorno de desarrollo como `STRIPE_SECRET_KEY` y `STRIPE_PUBLISHABLE_KEY`.

Para que el servicio pueda responder a las peticiones del proyecto, deberá escuchar al webhook de la aplicación local. Primero se debe descargar la herramienta CLI de Stripe, desde `https://github.com/stripe/stripe-cli/releases/tag/v1.22.0`, descargando el `stripe_1.22.0_windows_x86_64.zip`. Este se debe descomprimir en una carpeta del ordenador. Una vez hecho, se debe añadir al PATH del sistema: En variables del sistema, seleccionando la de Path, se añade la ruta al .exe descomprimido. Lo siguiente es abrir una consola y colocarse en la carpeta descomprimida. Escribiendo `stripe.exe` se ejecutará. A continuación se debe escribir el comando `stripe login`. Esto abrirá un navegador para iniciar sesión con la cuenta de stripe. Por último, con el comando `stripe listen --foward-to http://localhost:8000/pedidos/webhook/` establecerá la conexión que necesitamos. Esto devolverá un token para el webhook que se debe poner en el env como `STRIPE_WEBHOOK_SECRET`.

#### 8.2 Stripe para la imagen Docker en local

Será necesario seguir los pasos detallados en el apartado anterior, sobre la parte de la creación de stripe e inicialización del webhook local. Para insertar las variables de entorno en la imagen, 