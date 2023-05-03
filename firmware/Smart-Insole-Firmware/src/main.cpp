#include <Arduino.h>

const uint8_t ADDRESS_PINS[] = {14, 15, 27, 26};
const uint8_t SENSOR_PIN = 25;
const uint8_t ENABLE_PIN = 4;

uint16_t pressureValues[16];

void readValuesFromMUX(const uint8_t *addressPins, const uint8_t sensorPin,
                       uint16_t *sensorValues);
void printPressureValues();

void setup() {
    Serial.begin(115200);

    // ... Enable MUX
    pinMode(ENABLE_PIN, OUTPUT);
    digitalWrite(ENABLE_PIN, LOW);

    // ... Configure MUX
    for (int i = 0; i < 4; ++i) {
        pinMode(ADDRESS_PINS[i], OUTPUT);
    }
}

void loop() {
    readValuesFromMUX(ADDRESS_PINS, SENSOR_PIN, pressureValues);
    printPressureValues();
    delay(1000);
}

void readValuesFromMUX(const uint8_t *addressPins, const uint8_t sensorPin,
                       uint16_t *sensorValues) {
    for (int ch = 0; ch < 16; ++ch) {
        for (int i = 0; i < 4; ++i) {
            digitalWrite(addressPins[i], bitRead(ch, i));
        }
        sensorValues[ch] = analogRead(sensorPin);
    }
}

void printPressureValues() {
    for (int i = 0; i < 16; ++i) {
        Serial.print(pressureValues[i]);
        if (i < 15) Serial.print(",");
    }
    Serial.println();
}