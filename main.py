# main.py
import network
import socket
import time
from machine import Pin, PWM

# Velocidade padrão (0 a 65535)
velocidade = 30000

# Pinos dos motores com PWM (conforme tabela)
# Ponte H 1
IN1 = PWM(Pin(25), freq=1000)  # Motor A1
IN2 = PWM(Pin(26), freq=1000)
IN3 = PWM(Pin(27), freq=1000)  # Motor A2
IN4 = PWM(Pin(13), freq=1000)
# Ponte H 2
IN5 = PWM(Pin(18), freq=1000)  # Motor B1
IN6 = PWM(Pin(19), freq=1000)
IN7 = PWM(Pin(21), freq=1000)  # Motor B2
IN8 = PWM(Pin(22), freq=1000)

# Funções de controle de movimento

def parar():
    IN1.duty_u16(0); IN2.duty_u16(0); IN3.duty_u16(0); IN4.duty_u16(0)
    IN5.duty_u16(0); IN6.duty_u16(0); IN7.duty_u16(0); IN8.duty_u16(0)

def frente():
    IN1.duty_u16(velocidade); IN2.duty_u16(0)
    IN3.duty_u16(velocidade); IN4.duty_u16(0)
    IN5.duty_u16(velocidade); IN6.duty_u16(0)
    IN7.duty_u16(velocidade); IN8.duty_u16(0)

def tras():
    IN1.duty_u16(0); IN2.duty_u16(velocidade)
    IN3.duty_u16(0); IN4.duty_u16(velocidade)
    IN5.duty_u16(0); IN6.duty_u16(velocidade)
    IN7.duty_u16(0); IN8.duty_u16(velocidade)

def esquerda():
    IN1.duty_u16(0); IN2.duty_u16(velocidade)
    IN3.duty_u16(velocidade); IN4.duty_u16(0)
    IN5.duty_u16(velocidade); IN6.duty_u16(0)
    IN7.duty_u16(0); IN8.duty_u16(velocidade)

def direita():
    IN1.duty_u16(velocidade); IN2.duty_u16(0)
    IN3.duty_u16(0); IN4.duty_u16(velocidade)
    IN5.duty_u16(0); IN6.duty_u16(velocidade)
    IN7.duty_u16(velocidade); IN8.duty_u16(0)

# Configuração do Ponto de Acesso Wi-Fi
SSID = "Teste Robô ESP32"
PASSWORD = "12349876"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD, authmode=3)

while not ap.active():
    pass

print("Ponto de acesso Wi-Fi ativado!")
print(f"Conecte-se à rede: {SSID}")
print(f"IP do ESP32: {ap.ifconfig()[0]}")

# HTML da interface

def pagina_web():
    return """<!DOCTYPE html>
<html>
<head><title>Controle Robô ESP32</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    button { padding: 15px 30px; margin: 10px; font-size: 16px; }
</style>
</head>
<body>
    <h1>Controle do Robô 🤖</h1>
    <button onclick=\"enviar('frente')\">Frente</button><br>
    <button onclick=\"enviar('esquerda')\">Esquerda</button>
    <button onclick=\"enviar('direita')\">Direita</button><br>
    <button onclick=\"enviar('tras')\">Trás</button>
    <button onclick=\"enviar('parar')\">Parar</button>
    <script>
        function enviar(cmd) {
            fetch('/comando?dir=' + cmd);
        }
    </script>
</body>
</html>
"""

# Servidor Web
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)

print("Servidor Web iniciado!")

while True:
    try:
        cl, addr = s.accept()
        print(f"Cliente conectado: {addr}")
        request = cl.recv(1024).decode()

        if '/comando?dir=frente' in request:
            frente()
        elif '/comando?dir=tras' in request:
            tras()
        elif '/comando?dir=esquerda' in request:
            esquerda()
        elif '/comando?dir=direita' in request:
            direita()
        elif '/comando?dir=parar' in request:
            parar()

        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/html\n')
        cl.send('Connection: close\n\n')
        cl.sendall(pagina_web())
        cl.close()

    except Exception as e:
        print(f"Erro: {e}")
        cl.close()
