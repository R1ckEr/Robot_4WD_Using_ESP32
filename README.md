# 🤖 Robô Seguidor de Linha com ESP32

Este projeto implementa um robô seguidor de linha utilizando a placa ESP32, sensores infravermelhos, controle PWM via duas pontes H (L298N) e, opcionalmente, sensor ultrassônico para detecção de obstáculos. O código foi desenvolvido para garantir movimentos precisos, suaves e adaptativos mesmo em curvas fechadas e marcações especiais no percurso.

---

## 📂 Códigos Disponíveis

O repositório contém **quatro códigos disponíveis**, para níveis distintos de precisão e simplicidade:

- `Circuito2Sens.py`:  
  Utiliza **apenas 2 sensores infravermelhos** (esquerdo e direito). Ideal para testes iniciais ou trajetos simples.  
  **Menor precisão**, mas mais fácil de montar.

- `Circuito4Sens.py`:  
  Utiliza **4 sensores infravermelhos** (esquerdo, centro-esquerdo, centro-direito e direito).  
  **Maior precisão** nas curvas, ideal para movimentos certeiros e menos delay no movimento.

- `Ultrassonico2Sens.py`:  
  Utiliza **apenas 2 sensores infravermelhos** (esquerdo e direito) e **sensor ultrassônico** para detecção de obstáculos.   

- `Ultrassonico4Sens.py`:  
  Utiliza **4 sensores infravermelhos** (esquerdo, centro-esquerdo, centro-direito e direito) e **sensor ultrassônico** para detecção de obstáculos.  

---

## 🔧 Componentes Utilizados

| Componente                         | Quantidade   | Observações                                            |
|------------------------------------|--------------|--------------------------------------------------------|
| ESP32                              | 1            | Placa principal de controle                            |
| Ponte H L298N                      | 2            | Controle dos 4 motores DC com suporte a PWM            |
| Sensores Infravermelhos TCRT5000   | 2 ou 4       | Detectam a linha preta no chão                         |
| Sensor Ultrassônico HC-SR04        | 1 (opcional) | Detecta obstáculos à frente                            |
| Motores DC 3V–6V                   | 4            | Movimentação do robô                                   |
| Conversor DC/DC XL4015             | 1            | Alimentação dos motores, compensando queda nas pontes  |
| 4 Rodas e Chassis                  | 1 conjunto   | Montagem do robô                                       |
| Suporte 4 Pilhas AAA               | 2            | Suporte da Alimentação elétrica                        |
| Pilhas AAA 1,5V                    | 8            | Alimentação elétrica do robô                           |
| Mini Chave Gangorra - KCD11-101    | 1            | Liga/Desliga alimentação elétrica do robô              | 

---

## ⚙️ Pinagem Utilizada

### ✅ Sensores Infravermelhos (versão completa):
| Sensor            | Pino ESP32 |
|-------------------|------------|
| Esquerdo          | GPIO 34    |
| Centro-Esquerdo   | GPIO 35    |
| Centro-Direito    | GPIO 32    |
| Direito           | GPIO 33    |

---

### 🌐 Sensor Ultrassônico (HC-SR04):
| Função                   | Pino ESP32 |
|--------------------------|------------|
| TRIG                     | GPIO 12    |
| ECHO                     | GPIO 14    |

---

### 🔌 Ponte H L298N - Motores (com 2 L298N)

| Função                           | Pino ESP32 | Ponte H |
|----------------------------------|------------|----------|
| IN1 (Motor Esquerdo)             | GPIO 27    | Ponte A |
| IN2 (Motor Esquerdo)             | GPIO 26    | Ponte A |
| ENA (PWM - Motor Esquerdo)       | GPIO 25    | Ponte A |
| IN3 (Motor Direito)              | GPIO 19    | Ponte B |
| IN4 (Motor Direito)              | GPIO 18    | Ponte B |
| ENB (PWM - Motor Direito)        | GPIO 5     | Ponte B |

> As **duas pontes H** são utilizadas para maior estabilidade no controle dos motores, especialmente em condições de reversão e retomada.

---
## 🧠 Lógica de Funcionamento

- O robô segue uma linha preta utilizando sensores IR.
- Controle de velocidade via PWM garante curvas suaves e estabilidade em retas.
- Marcações no percurso (como "C|Ↄ") são identificadas com lógica de verificação antes da parada.
- Se o sensor ultrassônico detectar um obstáculo:
  - O robô **para**.
  - Dá **marcha ré**.
  - Retoma o trajeto após liberação do caminho.

---

## 🚀 Instruções de Uso

1. **Ajuste o Conversor DC/DC para ~7.5V** compensando a queda (~1.5V) nas pontes H.
2. **Conecte os sensores** conforme o código que deseja usar.
3. **Carregue o código no ESP32** com a IDE de sua preferência.
4. **Coloque o robô no percurso** e energize o sistema.
5. O robô seguirá automaticamente a linha.

---
## 📸 Imagens do Projeto

### Robô visto de cima
![Robô visto de cima](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_cima.jpg?raw=true)

### Robô de frente
![Robô de frente](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_frente.jpg?raw=true)

### Robô ligado e funcionando
![Robô ligado](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_ligado.jpg?raw=true)

---
## ✨ Créditos

Desenvolvido por **Ricardo Emanoel** como parte de um projeto IoT com ESP32.
