#include <Arduino.h>

#include "BluetoothSerial.h"

// ... Bluetooth Check
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled!
#endif

#if !defined(CONFIG_BT_SPP_ENABLED)
#error Serial Bluetooth not available or not enabled.
#endif

#define USE_PIN

const char *BT_PIN = "1234";
const char *DEVICE_NAME = "SMART_INSOLE_RIGHT";
const uint8_t ADDRESS_PINS[] = {14, 15, 27, 26};
const uint8_t SENSOR_PIN = 25;
const uint8_t ENABLE_PIN = 4;
uint16_t pressureValues[16];
char serializedPressureValues[100];

BluetoothSerial SerialBT;

void readValuesFromMUX(const uint8_t *addressPins, const uint8_t sensorPin,
                       uint16_t *sensorValues);
void serializePressureValues(char *buffer, uint16_t *pressureValues,
                             size_t nValues);
void printPressureValues();

void setup() {
    Serial.begin(115200);
    SerialBT.begin(DEVICE_NAME);
    Serial.printf("Deive %s is now Available\n", DEVICE_NAME);

#ifdef USE_PIN
    SerialBT.setPin(BT_PIN);
#endif

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
    serializePressureValues(serializedPressureValues, pressureValues, 16);
    SerialBT.println(serializedPressureValues);
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

void serializePressureValues(char *buffer, uint16_t *pressureValues,
                             size_t nValues) {
    buffer[0] = '\0';
    sprintf(buffer, "R: ");
    for (int i = 0; i < nValues; ++i) {
        sprintf(buffer + strlen(buffer), "%d", pressureValues[i]);
        if (i != nValues - 1) {
            sprintf(buffer + strlen(buffer), ",");
        }
    }
}

void printPressureValues() {
    for (int i = 0; i < 16; ++i) {
        Serial.print(pressureValues[i]);
        if (i < 15) Serial.print(",");
    }
    Serial.println();
}