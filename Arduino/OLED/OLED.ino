#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDRESS 0x3C

Adafruit_SH1106G display(
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  &Wire,
  -1
);

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);

  if (!display.begin(OLED_ADDRESS, true)) {
    Serial.println("SH1106 initialization failed");
    while (true) {
      delay(100);
    }
  }

  display.clearDisplay();
  display.display();
  delay(1000);

  display.setTextColor(SH110X_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 20);
  display.println("Hello World!");
  display.display();
}

void loop() {
}