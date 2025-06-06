// Bibliotecas Utilizadas
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

// Definições de Pinos 
#define TRIG_PIN 5
#define ECHO_PIN 18
#define CHUVA_PIN 19
#define LED_PIN 2
#define DHT_PIN 15
#define DHTTYPE DHT22
#define SDA_PIN 26  
#define SCL_PIN 25  

// Wi-Fi 
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Token do TagoIO 
const char* TAGO_TOKEN = "";

// Início
DHT dht(DHT_PIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(CHUVA_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  Wire.begin(SDA_PIN, SCL_PIN);
  //lcd está sendo usada apenas para testes internos
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("ChuvaSegura");
  lcd.setCursor(0, 1);
  lcd.print("Conectando...");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi: OK");
  delay(1000);
}

void loop() {
  // Medir nível da água
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duracao = pulseIn(ECHO_PIN, HIGH);
  float distancia_cm = duracao * 0.034 / 2;

  // Temperatura e Umidade
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();
  // Wokwi não simula sensores de chuva reais, então usamos um pino digital (CHUVA_PIN) 
  // que pode ser ligado ou desligado manualmente para testes. 
  // >>> PARA TESTAR manualmente como se estivesse sempre chovendo:
  // Basta forçar o valor da variável:
  // remova o "!" para ler o valor diretamente:
  // int chuva = digitalRead(CHUVA_PIN);
  int chuva = digitalRead(CHUVA_PIN);

  // Alertas Críticos
  bool alerta_agua = false;
  bool alerta_temp = false;
  bool alerta_umid = false;
  bool alerta_critico = false;

  if (distancia_cm < 10) {
    alerta_agua = true;
    Serial.println("⚠️ ALERTA: Nível de água muito alto!");
  }

  if (temperatura > 40.0) {
    alerta_temp = true;
    Serial.println("⚠️ ALERTA: Temperatura extrema!");
  }

  if (umidade > 95.0) {
    alerta_umid = true;
    Serial.println("⚠️ ALERTA: Umidade excessiva detectada!");
  }

  if (chuva && distancia_cm < 15) {
    alerta_critico = true;
    Serial.println("🚨 SITUAÇÃO CRÍTICA: CHUVA + NÍVEL ALTO!");
  }

  // LCD: Mensagem personalizada 
  lcd.clear();
  if (alerta_critico) {
    lcd.setCursor(0, 0);
    lcd.print("!! ALERTA TOTAL !!");
    lcd.setCursor(0, 1);
    lcd.print("Evacuar!");
  } else if (alerta_agua) {
    lcd.setCursor(0, 0);
    lcd.print("Nivel Critico!");
    lcd.setCursor(0, 1);
    lcd.print("A: ");
    lcd.print(distancia_cm, 0);
    lcd.print("cm");
  } else {
    lcd.setCursor(0, 0);
    lcd.print("A:");
    lcd.print(distancia_cm, 0);
    lcd.print("cm ");
    lcd.print(chuva ? "C" : "S"); // C = Chuva, S = Seco
    lcd.setCursor(0, 1);
    lcd.print((int)temperatura);
    lcd.print("C ");
    lcd.print((int)umidade);
    lcd.print("%");
  }

  // LED acende se houver alerta
  digitalWrite(LED_PIN, alerta_agua || alerta_temp || alerta_umid || alerta_critico ? HIGH : LOW);

  // Envio para TagoIO 
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("https://api.tago.io/data");
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Device-Token", TAGO_TOKEN);

    String payload = "[";
    payload += "{\"variable\":\"nivel_agua\",\"value\":" + String(distancia_cm) + "},";
    payload += "{\"variable\":\"temperatura\",\"value\":" + String(temperatura) + "},";
    payload += "{\"variable\":\"umidade\",\"value\":" + String(umidade) + "},";
    payload += "{\"variable\":\"chuva\",\"value\":" + String(chuva) + "}";
    payload += "]";

    int resposta = http.POST(payload);
    Serial.println("Resposta TagoIO: " + String(resposta));
    http.end();
  }

  delay(20000); 
}