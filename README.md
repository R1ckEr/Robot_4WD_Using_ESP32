# 🤖 Robô Seguidor de Linha 4WD com ESP32

Este projeto implementa um robô seguidor de linha com tração nas quatro rodas, utilizando MicroPython em um ESP32. O sistema conta com sensores infravermelhos para detecção de linha, controle de motores via PWM com duas pontes H (L298N) e, opcionalmente, um sensor ultrassônico para detecção de obstáculos ao longo do trajeto.


---

## 📂 Códigos Disponíveis

O repositório contém **quatro códigos disponíveis**, para níveis distintos de precisão e simplicidade:

- `Circuito2Sens.py`:  
  Utiliza **apenas 2 sensores infravermelhos** (esquerdo e direito). Ideal para trajetos simples.  
  **Menor precisão**, porém mais fácil de montar.

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
| 4 Rodas e Chassi                   | 1 conjunto   | Montagem do robô                                       |
| Suporte 4 Pilhas AAA               | 2            | Suporte da Alimentação elétrica                        |
| Pilhas AAA 1,5V                    | 8            | Alimentação elétrica do robô                           |
| Mini Chave Gangorra - KCD11-101    | 1            | Liga/Desliga alimentação elétrica do robô              | 

---

## 🔌 Pinagem dos Componentes

### 🔧 **Motores com PWM (Ponte H L298N)**

| Função                         | GPIO (ESP32) | Ponte H              |
|--------------------------------|--------------|----------------------|
| Motor Direito Traseiro Frente  | GPIO 25      | Ponte H 1 - Motor A1 |
| Motor Direito Traseiro Ré      | GPIO 26      | Ponte H 1 - Motor A1 |
| Motor Esquerdo Traseiro Ré     | GPIO 27      | Ponte H 1 - Motor A2 |
| Motor Esquerdo Traseiro Frente | GPIO 13      | Ponte H 1 - Motor A2 |
| Motor Esquerdo Frontal Frente  | GPIO 18      | Ponte H 2 - Motor B1 |
| Motor Esquerdo Frontal Ré      | GPIO 19      | Ponte H 2 - Motor B1 |
| Motor Direito Frontal Frente   | GPIO 21      | Ponte H 2 - Motor B2 |
| Motor Direito Frontal Ré       | GPIO 22      | Ponte H 2 - Motor B2 |

---

### 👀 **Sensores Infravermelhos**

| Sensor                     | GPIO (ESP32) |
|----------------------------|--------------|
| Sensor IR Esquerdo         | GPIO 34      |
| Sensor IR Centro-Esquerdo  | GPIO 35      |
| Sensor IR Centro-Direito   | GPIO 32      |
| Sensor IR Direito          | GPIO 33      |

---

### 📡 **Sensor Ultrassônico (HC-SR04)**

| Função     | GPIO (ESP32) |
|------------|--------------|
| TRIG       | GPIO 12      |
| ECHO       | GPIO 14      |

---

## 🔋 Alimentação

- 🔌 **Fonte**: 8 pilhas AAA (4 + 4 em série)
- 🔧 **Regulador Buck**: ajustado para 7.5V na saída e conectado nas Pontes H
- ⚠️ A alimentação do ESP32 e dos motores é separada, sendo o ESP32 alimentado com a saída **5V** de uma das **Pontes H**
- Todos os GNDs interligados (ESP32, Buck e Pontes H)

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

## 🔌 Diagrama do Circuito

O diagrama abaixo mostra todas as conexões elétricas realizadas no projeto, incluindo:

- Alimentação via 8 pilhas AAA conectadas em série em um buck converter.
- Conexão de todos os motores às duas pontes H.
- Conexão elétrica dos sensores utilizados (exceto conexões lógicas)

### 📷 Visualização:

![Diagrama Completo](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/diagrama_completo.JPG)

### 📂 Download do arquivo editável (.fzz):

Você pode baixar o arquivo editável para abrir no Fritzing clicando abaixo:

👉 [`diagrama.fzz`](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/raw/imagens/diagrama.fzz)

---

## 📸 Imagens do Projeto

### Robô visto de cima
![Robô visto de cima](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_cima.jpg?raw=true)

### Robô de frente
![Robô de frente](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_frente.jpg?raw=true)

### Robô ligado
![Robô ligado](https://github.com/R1ckEr/Robot_4WD_Using_ESP32/blob/imagens/Robo_ligado.jpg?raw=true)

---
## 👥 Créditos

Projeto desenvolvido por:

- [Ricardo Ribeiro](https://www.linkedin.com/in/rick-er/)
- [Bruno Miam](https://www.linkedin.com/in/brunomiam/)
- [Nathaly Vieira](https://www.linkedin.com/in/nathaly-r-vieira-15a554363/)
- [Mayara Souza](https://www.linkedin.com/in/mayara-cssouza/)

Este projeto foi desenvolvido como parte da nossa graduação em Defesa Cibernética, na disciplina de IoT, com foco em aplicações práticas de automação e robótica.

