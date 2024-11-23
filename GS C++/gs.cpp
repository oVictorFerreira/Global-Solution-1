#include <Servo.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

Servo servoMotor;
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int ldrPin = A0;
const int ledPin = 8;
const int trigPin = 6;
const int echoPin = 7;


int luzAtual = 0;
int anguloAtual = 90;

void setup() {

  servoMotor.attach(9);
  dht.begin();
  lcd.init();
  lcd.backlight();
  pinMode(ldrPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);


  servoMotor.write(anguloAtual);
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  delay(2000);
}

void loop() {

  luzAtual = analogRead(ldrPin);

  if (luzAtual < 500 && anguloAtual < 180) {
    anguloAtual += 10;
  } else if (luzAtual > 700 && anguloAtual > 0) {
    anguloAtual -= 10;
  }
  servoMotor.write(anguloAtual);


  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  if (luzAtual < 400 || umidade > 70) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }


  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Luz: ");
  lcd.print(luzAtual);
  lcd.setCursor(0, 1);
  lcd.print("T: ");
  lcd.print(temperatura);
  lcd.print("C");
  lcd.setCursor(10, 1);
  lcd.print("U: ");
  lcd.print(umidade);

  delay(1000);
}