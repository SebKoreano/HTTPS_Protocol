# HTTPS_Protocol

Este repositorio contiene un ejemplo práctico en Python de una aplicación cliente-servidor que ilustra la diferencia entre comunicaciones **HTTP** no cifradas y **HTTPS/TLS** cifradas. Incluye:

- Generación automática de un certificado autofirmado (`cert.pem` / `key.pem`).  
- Servidor que acepta primero conexiones HTTP en texto claro y luego HTTPS con TLS.  
- Cliente que conecta por HTTP y luego por HTTPS, mostrando en consola:  
  - Proceso de handshake TLS.  
  - Inspección del certificado del servidor.  
  - Envío, recepción y descifrado de mensajes.

---

## Contenido

- `server.py` – Código del servidor que:  
  1. Genera el certificado si no existe.  
  2. Atiende un puerto HTTP (texto claro).  
  3. Atiende un puerto HTTPS (TLS) e imprime el handshake, el cifrado negociado y los mensajes descifrados.
- `client.py` – Código del cliente que:  
  1. Se conecta al servidor por HTTP, envía y recibe un mensaje en claro.  
  2. Se conecta al servidor por HTTPS, realiza el handshake, muestra el certificado y el cifrado, y transmite un mensaje cifrado.

---

## Requisitos

- Python 3.6+  
- OpenSSL instalado en el sistema (para la generación del certificado).  

---

## Cómo usar

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/<tu-usuario>/python-http-https-demo.git
   cd python-http-https-demo
