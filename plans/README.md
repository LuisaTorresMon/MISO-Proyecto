# Microservicio Offers

## Tabla de contenido

1. [Pre-requisitos](#pre-requisito-rutas)
2. [Estructura microservicio](#estructura-rutas)
   - [Archivos de soporte](#archivos-de-soporte)
   - [Carpeta main](#carpeta-main)
   - [Carpeta test](#carpeta-test)
3. [Ejecutar microservicio](#ejecutar-rutas)
   - [Instalar dependencias](#instalar-dependencias)
   - [Variables de entorno](#variables-de-entorno)
   - [Ejecutar aplicacion](#ejecutar-aplicacion)
   - [Ejecutar pruebas](#ejecutar-pruebas)
     - [Verificar coverage en pipeline](#cobertura-pipeline-rutas)
   - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
   - [Ejecutar Docker Compose](#ejecutar-docker-compose)
4. [Uso](#uso-rutas)
   - [Consumir la API](#consumir-la-api)
6. [Autor](#autor-rutas)

<a name="pre-requisito-rutas"></a>

### 1. Pre-requisitos

- Python 3.9 
- Pipenv 
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

<a name="estructura-rutas"></a>

## 2. Estructura

Inicialmente la estructura de proyecto esta distribuida de la siguiente manera:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/b7d37e38-fa4f-47c9-843c-3965e53f6fa8)

El microservicio utiliza Python y flask para ejecutar el servidor, y Pytest para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` el cual contiene la logica de la aplicación y 1 carpeta test `test` para ejecutar las pruebas unitarias, así como algunos archivos de soporte.

### Archivos de soporte

- `Pipfile`: archivo de configuración de nuestra aplicacion de Python el cual contiene las dependiencias necesarias para su correcto funcionamiento, por ejemplo flask, SQlalquemy, pytest, etc.
- `Pipfile.lock`: archivo de detalle de las dependencias, el cual se crea automaticamente cuando ejecuto el comando Pipenv install.
- `Dockerfile`: archivo de configuración de Docker para crear una imagen a partir de nuestra aplicación.
- `.env.template`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente "productivo".
- `.env.test`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente de pruebas.

### Carpeta main

- En la raiz de la carpeta '/src' tenemos el archivo main.py el cual contiene la la configuración inicial de la aplicación y al declaración de sus servicios controladores.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/cd678830-f3df-4f18-a64b-9f1968f40fd5)

- En la carpeta '/blueprints' existe un archivo llamado operations.py el cual contiene cada uno de los servicios a exponer.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/8f3deddd-5435-4030-8817-c48c233a7f67)

- En la carpeta '/validators' existe un archivo llamado validator.py el cual contiene las validaciones para cada servicio, como validar el token, validar los campos faltantes, formatos de campos, etc.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/44f7c426-28d5-45ce-a26b-af3a71cc2238)

- En la carpeta '/commands' existen archivos como create.py, delete.py, get.py, list.py y reset.py, los cuales contienen la logica de negocio y transaccionabilidad, como crear oferta, consultar ofertas, eliminar ofertas, etc.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/59be477a-80c3-4bd5-a843-5b2113cc5d09)

- En la carpeta '/errors' tenemos un archivo llamado un archivo llamado errors.py el cual contiene todas las excepciones personalizadas las cuales estan creadas para devolver el codigo y mensaje solcitado en el enunciado.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/0ab640dd-2a98-4fbb-912c-903bd0f2e580)

- En la carpeta '/models' tenemos un archivo llamado models.py el cual contiene la entidad Offers y schema asociado para la respectiva trasnformación a json.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/48ca347b-1e11-4063-8cc7-b530bd8e0f34)

### Carpeta test

- En la ruta test tenemos un archivo en la raiz llamado conftest.py, este archivo nos permite configurar que los test tomen las variables de entorno de el archivo .env.test, para que la base de datos levante con la base de datos de memoria

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/5213e11b-b19e-4cf7-a3b7-2f0728f24f32)

- En el folder '/blueprints' tenemos un archivo llamado 'test_offers_operation.py' el cual contiene las pruebas.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/18680682-98c6-4b24-8128-fc421a53fa81)

<a name="ejecutar-rutas"></a>

## 3. Ejecutar microservicio

### Instalar dependencias

- Activamos el entorno virtual, ejecutando el comando .\venv\Scripts\Activate, cuando se active, podremos ver desde la consola (venv)

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/221f165a-6e3f-43e4-b104-cac279f2574a)

- En la carpeta raiz ejecutamos el comando 'pipenv install'

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/371803bc-00c0-4275-8728-0a0614ced3a8)

### Variables de entorno

Nuestra aplicación utiliza variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución, esas variables son:

- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

### Ejecutar aplicacion

Para ejecutar la aplicación nos situamos en la carpeta raíz del repositorio y ejecutamos 'docker compose up', ya que debemos consumir el microservicio de users:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/a115eaa7-8e0e-45b2-b24a-ce10d8797666)

Al subir todo, nos debe salir así y podemos ver que podemos consumir nuestro microservicio por el puerto 3003

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/fa01ad3b-3362-417d-97bc-74bf8dac570c)

### Ejecutar pruebas

Para ejecutar las pruebas unitarias del microservicios ejecuta el comando 'python -m pytest tests' desde la carpeta raíz del microservicio offers, en la consola podremos ver si las pruebas fueron exitosas:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/9b87d8c4-f21a-409d-9849-625411e57a35)

Tambien podemos ejecutar el comando 'pytest .\tests\blueprints\test_offers_operations.py --cov-fail-under=70 --cov=src --cov-report=html' si queremos evidenciar el porcentaje de cobertura, especificando que este debe ser mayor de 70%

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/2562c65d-c26a-41f9-bba4-740a12e63c33)

<a name="cobertura-pipeline-rutas"></a>

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática cuando se realiza push a la rama main y generará un error cuando la cobertura
de código - coverage no supere el 70%.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/ba7bd9af-8131-479a-b8e3-cf63c1d52c77)

Resultado:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/d89b6de9-ecc4-4fe5-b14d-e99f1652b730)

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/e6765236-ba2f-4af9-bd7e-ecaa34a25a7c)

### Ejecutar desde Dockerfile
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:
```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecutar Docker Compose
Para ejecutar todos los microservicios al mismo tiempo, utilizamos docker-compose para declarar y configurar cada Dockerfile de los microservicios. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

<a name="uso-rutas"></a>

## 4. Uso

### Consumir la API
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega3/entrega3.json

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">


<a name="autor-rutas"></a>

## 6. Autor
Luisa Johanna Torres Moncaleano - lj.torresm1@uniandes.edu.co
