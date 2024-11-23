
# **Rastreador Solar Automatizado com Monitoramento Ambiental**

João Victor da Silva Ferreira - RM 560439
Erick Cardoso - RM 560440
Davi Daparé - RM 560721

### **Descrição do Projeto**
Este projeto utiliza um Arduino Uno para criar um rastreador solar automatizado que ajusta a posição de um painel solar em direção à maior luminosidade, ajudando a maximizar a captação de energia solar. Além disso, monitora temperatura, umidade e intensidade da luz, exibindo as informações em um display LCD. Um LED indica condições desfavoráveis, como baixa luminosidade ou alta umidade.

---

### **Componentes Utilizados**
- **Arduino Uno**
- **Sensor de luminosidade (LDR)**
- **Sensor de temperatura e umidade (DHT11 ou DHT22)**
- **Servomotor**
- **Display LCD 16x2 com I2C**
- **LED (indicador de condições)**
- **Sensor ultrassônico HC-SR04 (opcional)**
- Protoboard, resistores, cabos e outros componentes básicos.

---

### **Funcionalidades**
1. **Rastreamento Solar**: Ajusta automaticamente o ângulo do painel para a posição de maior luminosidade.
2. **Monitoramento Ambiental**:
   - Temperatura e umidade exibidas no LCD.
   - Intensidade da luz também monitorada.
3. **Alerta de Condições Desfavoráveis**: O LED acende se:
   - A luz for insuficiente.
   - A umidade for muito alta.
4. **Evitar Obstáculos**: Usa o sensor ultrassônico para detectar colisões.

---

### **Esquema de Conexão**
1. **LDR**: 
   - Um lado → 5V; outro lado → resistor de 10kΩ → GND; leitura analógica → A0.
2. **DHT**: 
   - Pino de dados → D2.
3. **Servomotor**: 
   - Sinal → D9.
4. **LCD**: 
   - SDA → A4; SCL → A5.
5. **LED**:
   - Anodo → D8; catodo → resistor (220Ω) GND.
6. **Sensor Ultrassônico**:
   - Trigger → D6; Echo → D7.

---

### **Instalação**
1. Instale as bibliotecas necessárias na IDE do Arduino:
   - `DHT.h` (para o sensor de temperatura e umidade).
   - `LiquidCrystal_I2C.h` (para o LCD I2C).
   - `Servo.h` (para o servomotor).
2. Faça as conexões conforme o esquema.
3. Carregue o código fornecido no Arduino Uno.

---

### **Uso**
1. Ligue o Arduino Uno.
2. Observe as medições exibidas no display LCD:
   - Temperatura, umidade e luminosidade.
3. O painel ajustará automaticamente sua posição.
4. O LED acenderá caso condições desfavoráveis sejam detectadas.
