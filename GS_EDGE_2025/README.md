# Global Solution - Edge

##  Integrantes
- Davi Daparé RM: 560721  
- Erick Cardoso RM: 560440  
- João Victor Ferreira RM: 560439  

## Ideia do Projeto Geral
Rede social para colaboração e alerta de enchentes.  
A proposta é uma plataforma digital interativa, uma rede social comunitária, voltada à prevenção, monitoramento e resposta a enchentes.  
Usuários podem registrar relatos em tempo real sobre alagamentos, obstruções de vias, níveis de água e situações de risco, geolocalizados em um mapa interativo.

## Aplicação com Arduino
Sistema de monitoramento de galerias e bueiros, utilizando sensor ultrassônico acoplado ao ESP32.  
O sensor mede o nível da água e envia os dados via MQTT. A ideia é integrar futuramente à plataforma TagoIO, que exibe os dados em tempo real em um dashboard.

### Benefícios
- Monitoramento em tempo real do nível da água.
- Visualização local via LCD.
- Publicação automática via MQTT.
- Possibilidade de gerar alertas automáticos preventivos.

## Componentes Utilizados
- ESP32  
- Sensor Ultrassônico HC-SR04  
- LCD 16x2 com I2C  
- Conexão Wi-Fi  
- MQTT Broker (test.mosquitto.org)  

## Link Wokwi
[Simulação no Wokwi](https://wokwi.com/projects/)

## Bibliotecas Utilizadas
```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
```

## Pinos e Configurações
- TRIG: GPIO 5  
- ECHO: GPIO 18  
- LCD I2C: Endereço `0x27`, 16 colunas, 2 linhas  
- Wi-Fi SSID: `Wokwi-GUEST`  
- Broker MQTT: `test.mosquitto.org` na porta 1883  
- Tópico MQTT: `test_topic_challenge`  

## Lógica de Funcionamento

1. Inicia conexão com Wi-Fi e MQTT.
2. Lê a distância do sensor ultrassônico.
3. Classifica o nível da galeria como:
   - `Cheio` (<= 20 cm)  
   - `Médio` (entre 21 cm e 150 cm)  
   - `Vazio` (> 150 cm)
4. Cria um JSON com a distância e status.
5. Publica no MQTT.
6. Mostra no LCD.

## Código-Fonte
Disponível no Wokwi, mas será migrado para o GitHub com modularização futura.

## Fluxograma
```text
[Início] → [Conectar Wi-Fi] → [Conectar MQTT]  
→ [Loop principal]  
  ├─> [Ler distância]  
  ├─> [Classificar nível]  
  ├─> [Gerar JSON]  
  ├─> [Publicar MQTT]  
  └─> [Exibir no LCD]  
```

## 🖼️ Imagens de Simulação

![Montagem no Wokwi](https://github.com/user-attachments/assets/e6a53b07-fd96-4a7c-ae4d-1f4a229d7356)
![Fluxograma]()

## Links Externos
- [Documentação Técnica](https://docs.google.com/document/d/1Z9Fu4Gfrlv3Qu_EUzGQVUTOyZfjbj4FEVXcCdOAh9mo/edit?usp=sharing)  
- [Pitch](https://youtu.be/HGWAP5JJgus?si=1-d8mfUoh8zn4iuJ)  
- [Explicação Técnica](https://youtu.be/DLxI929asmE?si=DxZKBtdCEC7qwx2J)
