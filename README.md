# proyecto-base  

## Tabla de contenido

- [Pre-requisitos para cada microservicio](#pre-requisitos-para-cada-microservicio)
- [Ejecutar Docker Compose](#ejecutar-docker-compose)
- [Ejecutar Colección de Postman](#ejecutar-colección-de-postman)
- [Ejecutar evaluador github action workflow](#ejecutar-evaluador-github-action-workflow)

## Pre-requisitos para cada microservicio

### Microservicio de usuarios 
<a name="pre-requisito-usuarios"></a>

- openjdk 17:Temurin
	- Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://adoptium.net/temurin/releases/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

### Microservicio de trayectos 
- Python ~3.10
- pipenv
    - Ejecuta `pip install pipenv` para instalarlo
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

### Microservicio de publicaciones
- Python ~3.10
- pipenv
    - Ejecuta `pip install pipenv` para instalarlo
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

### Microservicio de ofertas 
- Python ~3.10
- pipenv
    - Ejecuta `pip install pipenv` para instalarlo
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

## Ejecutar Docker Compose
Para ejecutar todos los microservicios al mismo tiempo, utilizamos docker-compose para declarar y configurar cada Dockerfile de los microservicios. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

## Ejecutar Colección de Postman
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

## Ejecutar evaluador github action workflow

Para las entregas 1 y 2, hemos proporcionado un evaluador automático que ejecutará validaciones en los servicios API expuestos en cada entrega. Este evaluador se ejecuta como un workflow de Github Actions en el repositorio. Para ejecutar el workflow, ve a la sección de "Actions" del repositorio que se encuentra en la parte superior.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/92d686b7-21b1-42b1-b23a-e8c3d626dfd3" alt="Screenshot" width="800">

Luego, encontrarás en la sección izquierda una lista de todos los flujos de trabajo (workflows) disponibles para ejecución. En este caso, verás "Evaluator_Entrega1" y "Evaluator_Entrega2", correspondientes a los evaluadores de las dos primeras entregas. Haz clic en el que deseas ejecutar. Verás un botón "Run workflow" en la sección superior derecha, haz clic en este botón, selecciona la rama en la que deseas ejecutarlo y haz clic en el botón "Run workflow".

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/4bcf1c0d-e422-4f9d-9ff6-a663f8248352" alt="Screenshot" width="800">

Esto iniciará la ejecución del workflow en la rama. Si todo funciona correctamente y la entrega es correcta, verás que todas las comprobaciones aparecen como aprobadas (passed).

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/c6c580b2-80e0-411d-8971-a252312ce5ea" alt="Screenshot" width="800">
