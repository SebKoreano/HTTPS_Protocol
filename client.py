import socket, ssl, pprint

HOST = 'localhost'
PORT_HTTP = 9999
PORT_HTTPS = 10000

# 1. Conexión y comunicación por HTTP (sin cifrado)
print("Cliente: Conectando al servidor vía HTTP...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT_HTTP))
mensaje = "Hello from HTTP Client"
sock.send(mensaje.encode('utf-8'))
print(f"Cliente (HTTP): Mensaje enviado: \"{mensaje}\"")
respuesta = sock.recv(1024)
if respuesta:
    print("Cliente (HTTP): Respuesta recibida:", respuesta.decode('utf-8', errors='ignore'))
sock.close()
print("Cliente: Conexión HTTP cerrada\n")

# 2. Conexión y comunicación por HTTPS (TLS)
print("Cliente: Conectando al servidor vía TLS/HTTPS...")
# Configurar contexto SSL sin verificación de certificado (autofirmado)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
# Envolver socket con TLS
ssl_sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                               server_hostname="localhost",
                               do_handshake_on_connect=False)
ssl_sock.connect((HOST, PORT_HTTPS))
print("Cliente: Iniciando handshake TLS...")
ssl_sock.do_handshake()
print("Cliente: Handshake TLS completado exitosamente")
# Inspeccionar certificado del servidor
cert = ssl_sock.getpeercert()
if cert:
    print("Cliente: Certificado del servidor:", pprint.pformat(cert))
else:
    # Si verify_mode=CERT_NONE, getpeercert() puede venir vacío; obtener en binario
    raw_cert = ssl_sock.getpeercert(binary_form=True)
    if raw_cert:
        cert_pem = ssl.DER_cert_to_PEM_cert(raw_cert)
        print("Cliente: Certificado del servidor (formato PEM):\n", cert_pem)
# Mostrar cifrado negociado
cipher = ssl_sock.cipher()
if cipher:
    print(f"Cliente: Cifrado negociado: {cipher[0]} ({cipher[1]})")
# Enviar mensaje cifrado al servidor
mensaje = "Hello from HTTPS Client"
ssl_sock.send(mensaje.encode('utf-8'))
print(f"Cliente (TLS): Mensaje enviado: \"{mensaje}\" (viaje cifrado)")
# Recibir y mostrar respuesta del servidor (ya descifrada por ssl)
respuesta = ssl_sock.recv(1024)
if respuesta:
    print("Cliente (TLS): Respuesta recibida (descifrada):", respuesta.decode('utf-8', errors='ignore'))
ssl_sock.close()
print("Cliente: Conexión TLS cerrada")
