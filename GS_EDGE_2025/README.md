# 🌧️ AlagaNão! – Monitoramento Inteligente de Galerias

**Projeto GS 2025 – Edge Computing | 1ESPS**

---

## 👨‍💻 Integrantes

- João Victor da Silva Ferreira – RM 560439  
- Erick Cardoso – RM 560440  
- Davi Daparé – RM 560721  

---

## ❗ Problema

Redes de esgoto e galerias subterrâneas em áreas urbanas frequentemente transbordam em períodos de chuva intensa, resultando em alagamentos, danos materiais e riscos à saúde. A ausência de um sistema de monitoramento em tempo real dificulta a resposta preventiva da Defesa Civil.

---

## 💡 Solução: AlagaNão!

Desenvolvemos um sistema baseado em **ESP32** que realiza a leitura de sensores distribuídos pela cidade:

- **Ultrassônico**: mede o nível da água nas galerias subterrâneas  
- **DHT22**: monitora temperatura e umidade do ar  
- **Sensor de chuva digital**: detecta chuva em tempo real (simulado no Wokwi)

Os dados são enviados via **HTTP seguro** para a **plataforma TagoIO**, onde são visualizados em dashboards e acionam **alertas automáticos** por e-mail ou SMS para a Defesa Civil.

---

## 🧠 Lógica de Alerta

O sistema gera alertas com base em condições críticas:

- 🔸 `nivel_agua < 10cm` → **risco de transbordamento**  
- 🔸 `temperatura > 40°C` → **risco térmico em galerias**  
- 🔸 `umidade > 95%` → **ambiente saturado, chance de chuva**  
- 🔴 `chuva == 1 && nivel_agua < 15cm` → **ALERTA CRÍTICO de alagamento iminente**

Esses alertas:
- Acendem o **LED de emergência**  
- Atualizam o **display LCD** com instruções imediatas (ex: "Evacuar")  
- **Disparam notificações automáticas** para autoridades e usuários via TagoIO Actions  

---

## 🧰 Componentes Utilizados

### 📟 Camada IoT
- ESP32 DevKit  
- Sensor Ultrassônico (nível)  
- Sensor DHT22 (clima)  
- Sensor de chuva (simulado)  
- LCD 16x2 I2C  
- LED de alerta  

### ☁️ Back-End – TagoIO
- Buckets de dados (nível, temperatura, umidade, chuva)  
- Dashboards interativos com gráficos
- Ações automatizadas (email, SMS)  

### 🖥️ Aplicação
- Mapa com localização dos sensores  
- Gráficos semanais de variação de nível de água  
- Histórico de alertas e eventos  

---

## 📦 Estrutura do Código

### `setup()`
- Inicializa sensores, LCD, Wi-Fi  
- Exibe mensagens iniciais e conecta à internet  

### `loop()`
- Coleta dados dos sensores  
- Avalia risco e gera alertas  
- Atualiza LCD e LED  
- Envia os dados para a TagoIO via HTTP POST  
- Aguarda 20 segundos para novo ciclo  

---

## 🚨 Ações Automatizadas no TagoIO

A plataforma TagoIO permite configurar **Actions** para disparar alertas automáticos quando condições críticas são detectadas. Por exemplo:

> **Se `nivel_agua > 300cm` → Enviar e-mail para Defesa Civil com local e dados do sensor**

Isso permite **resposta imediata em áreas de risco**, com base nos dados reais enviados pelos dispositivos.

img

---

## 🧪 Execução

1. Acesse o Wokwi e carregue o código do projeto  
2. Verifique o Wi-Fi e insira o token do TagoIO  
3. Crie um device e configure um dashboard na TagoIO  
4. Visualize os dados em tempo real e ative as notificações por e-mail  

---

## 📎 Anexos

- `codigo.cpp`: Código completo do microcontrolador  
- [Simulação de sensores no Wokwi  ](https://wokwi.com/projects/432868844409069569)
- Dashboard TagoIO com gráficos e mapa!
- Fluxo de arquitetura do sistema  

---

## 📹 Demonstração

🔗 *Inserir link do vídeo explicativo aqui*

---

**AlagaNão!** – inteligência contra alagamentos nas cidades.
