#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Credenciais WiFi
const char* SSID = "Wokwi-GUEST";
const char* PASSWORD = "";

// Configuração MQTT
const char* BROKER_MQTT = "test.mosquitto.org";
const int BROKER_PORT = 1883;
const char* ID_MQTT = "ESP32_galeria_monitor";
const char* TOPIC_PUBLISH = "sensores/galeria/nivel";

// Pinos do sensor ultrassônico
#define TRIG_PIN 5
#define ECHO_PIN 18

// LCD I2C
const int LCD_COLUMNS = 16;
const int LCD_ROWS = 2;
LiquidCrystal_I2C lcd(0x27, LCD_COLUMNS, LCD_ROWS);

// Clientes WiFi e MQTT
WiFiClient espClient;
PubSubClient MQTT(espClient);

// Temporização para envio
unsigned long publishUpdate = 0;
const int PUBLISH_DELAY = 5000; 
const int TAMANHO_JSON = 200;

// Funções auxiliares
void setup_wifi();
void initMQTT();
void reconnectMQTT();
void reconnectWiFi();
void checkWiFiAndMQTT();
float readDistance();

void setup_wifi() {
  Serial.print("Conectando ao WiFi...");
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
}

void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.print("Conectando ao broker MQTT...");
    if (MQTT.connect(ID_MQTT)) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(MQTT.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void reconnectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\nWiFi reconectado!");
}

void checkWiFiAndMQTT() {
  if (WiFi.status() != WL_CONNECTED) reconnectWiFi();
  if (!MQTT.connected()) reconnectMQTT();
}

// Lê o nível da galeria com sensor ultrassônico
float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  float duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.0344 / 2;
}

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  setup_wifi();
  initMQTT();
}

void loop() {
  checkWiFiAndMQTT();
  MQTT.loop();

  if ((millis() - publishUpdate) >= PUBLISH_DELAY) {
    publishUpdate = millis();

    float distancia_cm = readDistance();
    String local_id = "Sensor_Galeria_01";
    String status_nivel;

    // Classifica o nível
    if (distancia_cm <= 15) {
      status_nivel = "Crítico";
    } else if (distancia_cm > 15 && distancia_cm <= 50) {
      status_nivel = "Alerta";
    } else {
      status_nivel = "Normal";
    }

    // Cria JSON para envio
    StaticJsonDocument<TAMANHO_JSON> doc;
    doc["local"] = local_id;
    doc["nivel_cm"] = distancia_cm;
    doc["status"] = status_nivel;

    char buffer[TAMANHO_JSON];
    serializeJson(doc, buffer);

    // Publica via MQTT
    MQTT.publish(TOPIC_PUBLISH, buffer);
    Serial.println(buffer);

    // Exibe no LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Nivel: " + String(distancia_cm, 1) + "cm");
    lcd.setCursor(0, 1);
    lcd.print("Status: " + status_nivel);
  }
}

