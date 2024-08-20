# Encrypted_Message

Encrypted_Message es un sistema de mensajería simple que utiliza sockets para la comunicación entre un cliente y un servidor. Además, el proyecto incluye la generación y gestión de claves RSA para asegurar la comunicación.

## Características

- Comunicación cliente-servidor usando sockets TCP.
- Generación de claves RSA para encriptación y desencriptación de mensajes.
- Soporte para múltiples clientes conectados simultáneamente.
- Sistema de administración de claves públicas autorizadas.

## Estructura del Proyecto

- `client.py`: Código del cliente que se conecta al servidor, envía y recibe mensajes.
- `server.py`: Código del servidor que maneja las conexiones de los clientes y transmite los mensajes entre ellos.
- `gen_key.py`: Script para generar las claves RSA para el servidor y los clientes.
- `add_key.py`: Script para añadir claves públicas a un archivo de claves autorizadas en el servidor.
- `test.py`: Script de prueba para verificar la funcionalidad de encriptación y desencriptación utilizando las claves generadas.

## Requisitos

- Python 3.x
- Librería `pycryptodome` para la generación y manejo de claves RSA.

Puedes instalar la librería necesaria con:

```bash
pip install pycryptodome
```
## Configuración y Uso
- 1. Generación de Claves
Primero, genera las claves RSA para el servidor y los clientes:

bash
```
python gen_key.py
```
Esto generará las siguientes claves:

Claves del servidor: server/key_private.pem y server/key_public.pem
Claves del cliente: client/key_private.pem y client/key_public.pem
- 2. Añadir Claves Públicas Autorizadas
Para autorizar a un cliente, añade su clave pública al archivo de claves permitidas en el servidor:

bash
```
python server/add_key.py client/key_public.pem server/allowed_keys.txt
```
- 3. Ejecutar el Servidor
Inicia el servidor para escuchar conexiones entrantes:

bash
```
python server.py
```
- 4. Conectar el Cliente
Inicia un cliente y conéctalo al servidor:

bash
```
python client.py [IP_del_servidor]
```
Si no especificas la IP, se usará 127.0.0.1 por defecto.

- 5. Probar Encriptación/Desencriptación
Puedes probar el proceso de encriptación y desencriptación con el script test.py:

bash
```
python test.py
```
Esto verificará que los mensajes pueden ser encriptados y desencriptados correctamente usando las claves generadas.

Notas
Asegúrate de que el servidor y los clientes utilicen las claves correctas para la encriptación y desencriptación de mensajes.
En este proyecto, los mensajes no están encriptados por defecto en la comunicación cliente-servidor. Puedes extender el código para integrar la encriptación RSA en la transmisión de mensajes.
Licencia

Este proyecto es de código abierto bajo la licencia MIT. Siéntete libre de modificar y mejorar el código.

## Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, no dudes en abrir un issue o enviar un pull request.
