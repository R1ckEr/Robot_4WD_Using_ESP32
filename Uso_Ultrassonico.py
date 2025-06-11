from machine import Pin, PWM
import time

# Sensores infravermelhos
IR_L = Pin(34, Pin.IN)   # Esquerda
IR_CL = Pin(35, Pin.IN)  # Centro-Esquerda
IR_CR = Pin(32, Pin.IN)  # Centro-Direita
IR_R = Pin(33, Pin.IN)   # Direita

# Pinos dos motores com PWM
# Ponte H 1
IN1 = PWM(Pin(25), freq=1000)
IN2 = PWM(Pin(26), freq=1000)
IN3 = PWM(Pin(27), freq=1000)
IN4 = PWM(Pin(13), freq=1000)
# Ponte H 2
IN5 = PWM(Pin(18), freq=1000)
IN6 = PWM(Pin(19), freq=1000)
IN7 = PWM(Pin(21), freq=1000)
IN8 = PWM(Pin(22), freq=1000)

# Velocidade base
VEL_BASE = 30000
VEL_CURVA = 15000  # velocidade reduzida para o lado interno da curva

# Movimento dos motores com controle individual
def mover_motor_esquerdo(frente, velocidade):
    if frente:
        IN1.duty_u16(velocidade)
        IN2.duty_u16(0)
        IN3.duty_u16(velocidade)
        IN4.duty_u16(0)
    else:
        IN1.duty_u16(0)
        IN2.duty_u16(velocidade)
        IN3.duty_u16(0)
        IN4.duty_u16(velocidade)

def mover_motor_direito(frente, velocidade):
    if frente:
        IN5.duty_u16(velocidade)
        IN6.duty_u16(0)
        IN7.duty_u16(velocidade)
        IN8.duty_u16(0)
    else:
        IN5.duty_u16(0)
        IN6.duty_u16(velocidade)
        IN7.duty_u16(0)
        IN8.duty_u16(velocidade)

def parar():
    for motor in [IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8]:
        motor.duty_u16(0)

# Função principal de seguidor de linha
def seguir_linha():
    while True:
        # Leitura dos sensores (0 = linha preta)
        L = not IR_L.value()
        CL = not IR_CL.value()
        CR = not IR_CR.value()
        R = not IR_R.value()

        # Curvas leves e suaves com controle proporcional simplificado
        if CL and CR and not L and not R:
            # Centro: em linha reta
            mover_motor_esquerdo(True, VEL_BASE)
            mover_motor_direito(True, VEL_BASE)

        elif CL and not CR:
            # Leve curva para direita
            mover_motor_esquerdo(True, VEL_BASE)
            mover_motor_direito(True, VEL_CURVA)

        elif CR and not CL:
            # Leve curva para esquerda
            mover_motor_esquerdo(True, VEL_CURVA)
            mover_motor_direito(True, VEL_BASE)

        elif L:
            # Curva forte para esquerda
            mover_motor_esquerdo(True, VEL_CURVA)
            mover_motor_direito(True, int(VEL_BASE * 1.2))

        elif R:
            # Curva forte para direita
            mover_motor_esquerdo(True, int(VEL_BASE * 1.2))
            mover_motor_direito(True, VEL_CURVA)

        elif not (L or CL or CR or R):
            # Fora da linha - procurar a linha
            mover_motor_esquerdo(False, VEL_CURVA)
            mover_motor_direito(True, VEL_CURVA)

        else:
            # Situação indefinida - parar
            parar()

        time.sleep(0.01)  # Delay curto para fluidez
