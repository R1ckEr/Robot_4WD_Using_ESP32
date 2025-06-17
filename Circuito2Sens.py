# main.py
from machine import Pin, PWM
import time

# Velocidade padrão (0 a 65535)
velocidade_padrao = 30000
velocidade_curva_leve = 35000

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

def esquerda_leve():
    direita_frente.duty_u16(velocidade_curva_leve); direita_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(velocidade_curva_leve); direita_traseira_tras.duty_u16(0)
    esquerda_frente.duty_u16(0); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(0); esquerda_traseira_tras.duty_u16(0)

def direita_leve():
    esquerda_frente.duty_u16(velocidade_curva_leve); esquerda_tras.duty_u16(0)
    esquerda_traseira_frente.duty_u16(velocidade_curva_leve); esquerda_traseira_tras.duty_u16(0)
    direita_frente.duty_u16(0); direita_tras.duty_u16(0)
    direita_traseira_frente.duty_u16(0); direita_traseira_tras.duty_u16(0)

# Loop principal para seguir linha
marcacao_contador = 0
ultimo_tempo_marcacao = 0

while True:
    E = sensor_esquerdo.value()
    CE = sensor_centro_esquerdo.value()
    CD = sensor_centro_direito.value()
    D = sensor_direito.value()

    # Detecção de marcação especial "C|Ↄ" (todos os sensores no preto)
    if E == 0 and CE == 0 and CD == 0 and D == 0:
        if time.ticks_diff(time.ticks_ms(), ultimo_tempo_marcacao) > 1000:
            marcacao_contador += 1
            ultimo_tempo_marcacao = time.ticks_ms()
            # continua andando por um breve tempo antes de qualquer ação futura
            frente()
            time.sleep(0.5)
            parar()
            time.sleep(0.5)
        continue

    # Lógica de decisão refinada
    if CE == 0 and CD == 0 and E == 0 and D == 0:
        frente()
    elif CE == 0 and CD == 1:
        esquerda_leve()
    elif CE == 1 and CD == 0:
        direita_leve()
    else:
        parar()

    time.sleep(0.05)
