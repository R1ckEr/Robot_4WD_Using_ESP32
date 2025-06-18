# main.py
from machine import Pin, PWM
import time

# Velocidade padrão (0 a 65535)
velocidade_padrao =25000
velocidade_curva_leve = 50000

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

# Sensores infravermelhos
sensor_esquerdo = Pin(34, Pin.IN)
sensor_centro_esquerdo = Pin(35, Pin.IN)
sensor_centro_direito = Pin(32, Pin.IN)
sensor_direito = Pin(33, Pin.IN)

# Sensor Ultrassônico
trig = Pin(12, Pin.OUT)
echo = Pin(14, Pin.IN)

# Função Medir distância
def medir_distancia():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    while echo.value() == 0:
        sinal_inicio = time.ticks_us()
    while echo.value() == 1:
        sinal_fim = time.ticks_us()

    duracao = time.ticks_diff(sinal_fim, sinal_inicio)
    distancia = (duracao * 0.0343) / 2
    return distancia

# Funções de movimento

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

def esquerda_leve():
    direita_frente.duty_u16(velocidade_curva_leve); direita_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(velocidade_curva_leve); direita_traseira_tras.duty_u16(0)
    esquerda_frente.duty_u16(0); esquerda_tras.duty_u16(velocidade_padrao)
    esquerda_traseira_frente.duty_u16(0); esquerda_traseira_tras.duty_u16(velocidade_padrao)

def direita_leve():
    esquerda_frente.duty_u16(velocidade_curva_leve); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(velocidade_curva_leve); esquerda_traseira_tras.duty_u16(0)
    direita_frente.duty_u16(0); direita_tras.duty_u16(velocidade_padrao)
    direita_traseira_frente.duty_u16(0); direita_traseira_tras.duty_u16(velocidade_padrao)


# Lógica
while True:    
    
    distancia = medir_distancia()
    if distancia < 15:
        parar()
        time.sleep(0.5)
        tras()
        time.sleep(0.7)
        parar()
        time.sleep(0.5)
        continue
    
    
    CE = sensor_centro_esquerdo.value()
    CD = sensor_centro_direito.value()
    
    if CE == 0 and CD == 0:
        frente()
    elif CE == 1 and CD == 0:
        esquerda_leve()
    elif CE == 0 and CD == 1:
        direita_leve()
    else:
        parar()

    time.sleep(0.1)
    time.sleep(0.05)

