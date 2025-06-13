# main.py
import network
import socket
import time
from machine import Pin, PWM

# Velocidade padrão (0 a 65535)
velocidade_padrao = 30000
velocidade_curva = 45000

# Pinos dos motores com PWM (conforme tabela)
# Ponte H 1
direita_traseira_frente = PWM(Pin(25), freq=1000)  # Motor A1
direita_traseira_tras = PWM(Pin(26), freq=1000)
esquerda_tras = PWM(Pin(27), freq=1000)  # Motor A2
esquerda_frente = PWM(Pin(13), freq=1000)
# Ponte H 2
esquerda_traseira_frente = PWM(Pin(18), freq=1000)  # Motor B1
esquerda_traseira_tras = PWM(Pin(19), freq=1000)
direita_frente = PWM(Pin(21), freq=1000)  # Motor B2
direita_tras = PWM(Pin(22), freq=1000)

# Funções de controle de movimento

def parar():
    direita_frente.duty_u16(0); direita_tras.duty_u16(0)
    esquerda_frente.duty_u16(0); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(0); esquerda_traseira_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(0); direita_traseira_tras.duty_u16(0)

def frente():
    direita_frente.duty_u16(velocidade_padrao); direita_tras.duty_u16(0)
    esquerda_frente.duty_u16(velocidade_padrao); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(velocidade_padrao); esquerda_traseira_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(velocidade_padrao); direita_traseira_tras.duty_u16(0)

def tras():
    direita_frente.duty_u16(0); direita_tras.duty_u16(velocidade_padrao)
    esquerda_frente.duty_u16(0); esquerda_tras.duty_u16(velocidade_padrao)
    esquerda_traseira_frente.duty_u16(0); esquerda_traseira_tras.duty_u16(velocidade_padrao)
    direita_traseira_frente.duty_u16(0); direita_traseira_tras.duty_u16(velocidade_padrao)

def esquerda():
    # Lado direito (IN1, IN7) anda para frente
    direita_frente.duty_u16(velocidade_curva); direita_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(velocidade_curva); direita_traseira_tras.duty_u16(0)
    #Lado esquerdo frontal (N3) para trás
    esquerda_frente.duty_u16(0); esquerda_tras.duty_u16(velocidade_padrao)
    # Lado esquerdo (IN5) anda para trás
    esquerda_traseira_frente.duty_u16(0); esquerda_traseira_tras.duty_u16(velocidade_padrao)

def direita():
    # Lado esquerdo (IN3 e IN5) anda para frente
    esquerda_frente.duty_u16(velocidade_curva); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(velocidade_curva); esquerda_traseira_tras.duty_u16(0)

    # Lado direito traseiro (IN7) anda para trás
    direita_frente.duty_u16(0); direita_tras.duty_u16(velocidade_padrao)
    # Lado direito frontal (IN1) para tras
    direita_traseira_frente.duty_u16(0); direita_traseira_tras.duty_u16(velocidade_padrao)

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
        print(f"Erro: {e}")
        cl.close()
