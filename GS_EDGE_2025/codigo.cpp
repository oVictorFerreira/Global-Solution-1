#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

// Pinos
#define TRIG_PIN 5
#define ECHO_PIN 18
#define SENSOR_CHUVA_PIN 19 //Hipotético pq no wokwi não existe sensor de chuva
#define LED_PIN 2
#define DHT_PIN 15
#define DHTTYPE DHT22
#define SDA_PIN 26
#define SCL_PIN 25

// Wi-Fi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Token da API TagoIO
const char* TAGO_TOKEN = "3b19755e-4ebb-45de-bb32-ebeacfb8bc6b";

DHT dht(DHT_PIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(SENSOR_CHUVA_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  lcd.setCursor(0, 1);
  lcd.print("Conectando Wi-Fi");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("#");
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Conexao OK!");
  delay(1000);
}

void loop() {
  // Medição ultrassônica
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duracao_echo = pulseIn(ECHO_PIN, HIGH);
  float nivel_agua = duracao_echo * 0.034 / 2;

  // DHT22 - Temperatura e Umidade
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();

  // Sensor de chuva (digital)
  int chuva_detectada = digitalRead(SENSOR_CHUVA_PIN);

  // Estados de alerta
  bool agua_perigosa = nivel_agua < 10;
  bool calor_excessivo = temp > 40;
  bool umidade_excessiva = umid > 80;
  bool alerta_total = (chuva_detectada && nivel_agua < 15);

  if (distancia_cm < 10) {
    alerta_agua = true;
    Serial.println("⚠️ ALERTA: Risco de transbordamento!");
  }

  if (temperatura > 40.0) {
    alerta_temp = true;
    Serial.println("⚠️ ALERTA: Risco térmico em galeria!");
  }

  if (umidade > 80.0) {
    alerta_umid = true;
    Serial.println("⚠️ ALERTA: Umidade excessiva detectada!");
  }

  if (chuva && distancia_cm < 15) {
    alerta_critico = true;
    Serial.println("🚨 SITUAÇÃO CRÍTICA: CHUVA + NÍVEL ALTO!");
  }

  // Atualiza LCD
  lcd.clear();
  if (alerta_total) {
    lcd.setCursor(0, 0);
    lcd.print("!! RISCO TOTAL !!");
    lcd.setCursor(0, 1);
    lcd.print("EVACUAR!");
  } else if (agua_perigosa) {
    lcd.setCursor(0, 0);
    lcd.print("NIVEL ALERTA");
    lcd.setCursor(0, 1);
    lcd.print("Alt: ");
    lcd.print(nivel_agua, 0);
    lcd.print("cm");
  } else {
    lcd.setCursor(0, 0);
    lcd.print("A:");
    lcd.print(nivel_agua, 0);
    lcd.print("cm ");
    lcd.print(chuva_detectada ? "C" : "S"); // C = Chuva, S = Seco
    lcd.setCursor(0, 1);
    lcd.print((int)temp);
    lcd.print("C ");
    lcd.print((int)umid);
    lcd.print("%");
  }

  // LED como indicador visual
  bool algum_alerta = agua_perigosa || calor_excessivo || umidade_excessiva || alerta_total;
  digitalWrite(LED_PIN, algum_alerta ? HIGH : LOW);

  // Envio dos dados via HTTP
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("https://api.tago.io/data");
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Device-Token", TAGO_TOKEN);

    String json = "[";
    json += "{\"variable\":\"nivel_agua\",\"value\":" + String(nivel_agua) + "},";
    json += "{\"variable\":\"temperatura\",\"value\":" + String(temp) + "},";
    json += "{\"variable\":\"umidade\",\"value\":" + String(umid) + "},";
    json += "{\"variable\":\"chuva\",\"value\":" + String(chuva_detectada) + "}";
    json += "]";

    int status = http.POST(json);
    Serial.println("Status HTTP: " + String(status));
    http.end();
  }

  delay(5000); // Aguarda 5 segundos
}
