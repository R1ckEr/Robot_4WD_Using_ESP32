# main.py
import network
import socket
import time

# Configurações do Ponto de Acesso Wi-Fi
SSID = "Teste Robô ESP32"
PASSWORD = "12349876"

# Função para criar a página HTML
def pagina_web():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Controle Robô ESP32</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f0f0;}
        h1 { color: #333; }
        .button-container { margin-top: 30px; }
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px;
            cursor: pointer;
            border-radius: 8px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            transition: 0.3s;
        }
        button:hover { background-color: #45a049; box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); }
        .btn-frente { background-color: #007bff;}
        .btn-frente:hover { background-color: #0056b3;}
        .btn-tras { background-color: #007bff;}
        .btn-tras:hover { background-color: #0056b3;}
        .btn-esquerda { background-color: #ffc107;}
        .btn-esquerda:hover { background-color: #d39e00;}
        .btn-direita { background-color: #ffc107;}
        .btn-direita:hover { background-color: #d39e00;}
        p { color: #555; font-size: 18px; }
    </style>
</head>
<body>
    <h1>Controle do Robô 🤖</h1>
    <div class="button-container">
        <button class="btn-frente" onclick="sendCommand('frente')">Frente</button><br>
        <button class="btn-esquerda" onclick="sendCommand('esquerda')">Esquerda</button>
        <button class="btn-direita" onclick="sendCommand('direita')">Direita</button><br>
        <button class="btn-tras" onclick="sendCommand('tras')">Trás</button>
    </div>
    <p id="status">Comando: Nenhum</p>

    <script>
        function sendCommand(direction) {
            document.getElementById('status').innerText = "Comando: " + direction.charAt(0).toUpperCase() + direction.slice(1);
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/comando?dir=" + direction, true);
            xhr.send();
        }
    </script>
</body>
</html>
"""
    return html

# Configuração do Ponto de Acesso
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD)

while not ap.active():
    pass

print("Ponto de acesso Wi-Fi ativado!")
print(f"Conecte-se à rede: {SSID}")
print(f"IP do ESP32: {ap.ifconfig()[0]}")

# Configuração do Socket para o servidor web
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reusar o endereço
s.bind(addr)
s.listen(5) # Espera até 5 conexões

print("Servidor web escutando na porta 80...")

while True:
    try:
        cl, addr_cl = s.accept()
        print(f"Cliente conectado de: {addr_cl}")
        request = cl.recv(1024)
        request_str = request.decode('utf-8')
        # print("Conteúdo da Requisição:") # Descomente para depuração
        # print(request_str) # Descomente para depuração

        comando = None
        if "/comando?dir=frente" in request_str:
            comando = "Frente"
        elif "/comando?dir=tras" in request_str:
            comando = "Trás"
        elif "/comando?dir=esquerda" in request_str:
            comando = "Esquerda"
        elif "/comando?dir=direita" in request_str:
            comando = "Direita"

        if comando:
            print(f"Botão {comando} Pressionado!")
            # Aqui você adicionaria a lógica para controlar os motores do robô
            # Exemplo:
            # if comando == "Frente":
            #     motor_frente()
            # elif comando == "Trás":
            #     motor_tras()
            # ... e assim por diante

        # Envia a página HTML como resposta
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/html\n')
        cl.send('Connection: close\n\n')
        cl.sendall(pagina_web())
        cl.close()
        print(f"Cliente {addr_cl} desconectado.")

    except OSError as e:
        cl.close()
        print(f"Erro de conexão ou socket: {e}")
    except KeyboardInterrupt:
        print("Servidor encerrado.")
        s.close()
        ap.active(False)
        break
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        if 'cl' in locals() and cl: # Garante que cl existe e está aberto antes de tentar fechar
            cl.close()