import socket, ssl, os, subprocess

HOST = 'localhost'
PORT_HTTP = 9999
PORT_HTTPS = 10000

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"

# Generar certificado autofirmado si no existe
if not (os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE)):
    print("Generando certificado autofirmado...")
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-nodes", "-out", CERT_FILE, "-keyout", KEY_FILE,
        "-days", "365", "-subj", "/CN=localhost"
    ], check=True)
    print("Certificado generado: cert.pem, key.pem")

# Crear socket HTTP y socket HTTPS
sock_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_https = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_https.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_http.bind((HOST, PORT_HTTP))
sock_https.bind((HOST, PORT_HTTPS))
sock_http.listen(1)
sock_https.listen(1)
print(f"Servidor escuchando en puertos {PORT_HTTP} (HTTP) y {PORT_HTTPS} (HTTPS)")

# 1. Esperar conexión HTTP (texto plano)
conn, addr = sock_http.accept()
print(f"Servidor: Conexión HTTP aceptada desde {addr}")
data = conn.recv(1024)
if data:
    message = data.decode('utf-8', errors='ignore')
    print(f"Servidor (HTTP): Mensaje recibido: \"{message}\"")
    # Enviar respuesta en texto claro
    response = f"Echo (HTTP): {message}"
    conn.send(response.encode('utf-8'))
    print("Servidor (HTTP): Respuesta enviada")
conn.close()
print("Servidor: Conexión HTTP cerrada\n")

# 2. Esperar conexión HTTPS (TLS)
# Configurar contexto SSL del servidor con el certificado
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
print("Servidor: Esperando conexión HTTPS...")
raw_sock, addr = sock_https.accept()
print(f"Servidor: Conexión HTTPS aceptada desde {addr}")
# Envolver el socket con TLS (iniciando handshake)
ssl_sock = context.wrap_socket(raw_sock, server_side=True, do_handshake_on_connect=False)
print("Servidor: Iniciando handshake TLS...")
ssl_sock.do_handshake()
cipher = ssl_sock.cipher()
print(f"Servidor: Handshake TLS completado. Cifrado negociado: {cipher[0]} ({cipher[1]})")
# Recibir mensaje cifrado (automáticamente descifrado por ssl)
data = ssl_sock.recv(1024)
if data:
    message = data.decode('utf-8', errors='ignore')
    print(f"Servidor (TLS): Mensaje recibido (descifrado): \"{message}\"")
    # Enviar respuesta cifrada
    response = f"Echo (TLS): {message}"
    ssl_sock.send(response.encode('utf-8'))
    print("Servidor (TLS): Respuesta enviada (cifrada)")
ssl_sock.close()
sock_http.close()
sock_https.close()
print("Servidor: Conexión HTTPS cerrada y servidor terminado")
