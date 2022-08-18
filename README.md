# Banza-app
## Challenge tecnico

Para el desarrollo de este challenge utilice:
- Python 3.10.0
- virtualenv 20.16.3

### Pre condicion:

1) Instalar virtualenv: 
>$ pip install virtualenv==20.16.3

2) Crear .env
>$ python -m virtualenv --clear .env

3) Activar el interprete
>$ source .env/Scripts/activate

### Correr tests
Para el testing utilice pytest, por lo que con el entorno activado:
>$ pytest

### Levantar la app
Para levantar la app utilicce [uvicorn](https://www.uvicorn.org/) como ASGI web server
>$ uvicorn app.main:app

## Docker

TBD -> la idea es proporcionar un docker compose para correr la app y con una db mysql