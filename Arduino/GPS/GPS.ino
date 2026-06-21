#include <TinyGPSPlus.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#include <SPI.h>
#include <SD.h>

// ======================================================
// OLED configuration
// ======================================================

#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define OLED_ADDRESS  0x3C

#define OLED_SDA 21
#define OLED_SCL 22

Adafruit_SH1106G display(
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  &Wire,
  -1
);

// ======================================================
// GPS configuration
// ======================================================

TinyGPSPlus gps;

#define gpsSerial Serial2

#define GPS_RX 16   // Connect to GPS TX
#define GPS_TX 17   // Connect to GPS RX

// ======================================================
// SD card configuration
// ======================================================

#define SD_CS   5
#define SD_SCK  18
#define SD_MISO 19
#define SD_MOSI 23

#define LOG_FILE "/gps_data.csv"

bool sdReady = false;

// ======================================================
// Timing
// ======================================================

unsigned long lastUpdate = 0;
bool gpsErrorPrinted = false;


// Print a two-digit number on the OLED
void displayTwoDigits(uint8_t number) {
  if (number < 10) {
    display.print('0');
  }

  display.print(number);
}


// Print a two-digit number into a file
void fileTwoDigits(File &file, uint8_t number) {
  if (number < 10) {
    file.print('0');
  }

  file.print(number);
}


void setup() {
  Serial.begin(115200);

  // ----------------------------------------------------
  // Start GPS
  // ----------------------------------------------------

  gpsSerial.begin(
    9600,
    SERIAL_8N1,
    GPS_RX,
    GPS_TX
  );

  // ----------------------------------------------------
  // Start OLED
  // ----------------------------------------------------

  Wire.begin(OLED_SDA, OLED_SCL);

  if (!display.begin(OLED_ADDRESS, true)) {
    Serial.println("SH1106 initialization failed");

    while (true) {
      delay(100);
    }
  }

  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);

  display.println("Starting system...");
  display.display();

  // ----------------------------------------------------
  // Start SD card
  // ----------------------------------------------------

  SPI.begin(
    SD_SCK,
    SD_MISO,
    SD_MOSI,
    SD_CS
  );

  sdReady = SD.begin(SD_CS, SPI);

  if (!sdReady) {
    Serial.println("SD card initialization failed");
  } else {
    Serial.println("SD card initialized");

    createCSVFile();
  }

  delay(1000);
}


void loop() {
  // Read all available GPS characters
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // Update OLED and SD card once every second
  if (millis() - lastUpdate >= 1000) {
    lastUpdate = millis();

    updateOLED();
    saveGPSData();
    printGPSDataToSerial();
  }

  // Check whether any GPS serial data is arriving
  if (
    millis() > 5000 &&
    gps.charsProcessed() < 10 &&
    !gpsErrorPrinted
  ) {
    Serial.println("No GPS data detected. Check GPS wiring.");

    gpsErrorPrinted = true;
  }
}


// ======================================================
// Create CSV file and header
// ======================================================

void createCSVFile() {
  bool fileAlreadyExists = SD.exists(LOG_FILE);

  File file = SD.open(LOG_FILE, FILE_APPEND);

  if (!file) {
    Serial.println("Could not open GPS log file");
    sdReady = false;
    return;
  }

  // Only add the header when the file is new
  if (!fileAlreadyExists) {
    file.println(
      "date,time_utc,latitude,longitude,"
      "satellites,altitude_m,speed_kmh,fix"
    );
  }

  file.close();

  Serial.print("Logging to: ");
  Serial.println(LOG_FILE);
}


// ======================================================
// Save GPS data
// ======================================================

void saveGPSData() {
  if (!sdReady) {
    return;
  }

  File file = SD.open(LOG_FILE, FILE_APPEND);

  if (!file) {
    Serial.println("Could not open GPS log file");
    sdReady = false;
    return;
  }

  // ----------------------------------------------------
  // Date: YYYY-MM-DD
  // ----------------------------------------------------

  if (gps.date.isValid()) {
    file.print(gps.date.year());
    file.print('-');

    fileTwoDigits(file, gps.date.month());
    file.print('-');

    fileTwoDigits(file, gps.date.day());
  }

  file.print(',');

  // ----------------------------------------------------
  // UTC time: HH:MM:SS
  // ----------------------------------------------------

  if (gps.time.isValid()) {
    fileTwoDigits(file, gps.time.hour());
    file.print(':');

    fileTwoDigits(file, gps.time.minute());
    file.print(':');

    fileTwoDigits(file, gps.time.second());
  }

  file.print(',');

  // ----------------------------------------------------
  // Latitude
  // ----------------------------------------------------

  if (gps.location.isValid()) {
    file.print(gps.location.lat(), 6);
  }

  file.print(',');

  // ----------------------------------------------------
  // Longitude
  // ----------------------------------------------------

  if (gps.location.isValid()) {
    file.print(gps.location.lng(), 6);
  }

  file.print(',');

  // ----------------------------------------------------
  // Satellites
  // ----------------------------------------------------

  if (gps.satellites.isValid()) {
    file.print(gps.satellites.value());
  }

  file.print(',');

  // ----------------------------------------------------
  // Altitude
  // ----------------------------------------------------

  if (gps.altitude.isValid()) {
    file.print(gps.altitude.meters(), 2);
  }

  file.print(',');

  // ----------------------------------------------------
  // Speed
  // ----------------------------------------------------

  if (gps.speed.isValid()) {
    file.print(gps.speed.kmph(), 2);
  }

  file.print(',');

  // ----------------------------------------------------
  // Fix status
  // ----------------------------------------------------

  if (gps.location.isValid()) {
    file.println("VALID");
  } else {
    file.println("NO_FIX");
  }

  // Ensure the data is written before closing
  file.flush();
  file.close();
}


// ======================================================
// Update OLED
// ======================================================

void updateOLED() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);

  display.println("GPS NEO-M8N");

  if (gps.location.isValid()) {
    display.print("Lat: ");
    display.println(gps.location.lat(), 6);

    display.print("Lon: ");
    display.println(gps.location.lng(), 6);
  } else {
    display.println("Lat: waiting...");
    display.println("Lon: waiting...");
  }

  display.print("UTC: ");

  if (gps.time.isValid()) {
    displayTwoDigits(gps.time.hour());
    display.print(':');

    displayTwoDigits(gps.time.minute());
    display.print(':');

    displayTwoDigits(gps.time.second());
    display.println();
  } else {
    display.println("--:--:--");
  }

  display.print("Sat: ");

  if (gps.satellites.isValid()) {
    display.println(gps.satellites.value());
  } else {
    display.println("--");
  }

  display.print("Fix: ");

  if (gps.location.isValid()) {
    display.println("VALID");
  } else {
    display.println("NO FIX");
  }

  display.print("SD: ");

  if (sdReady) {
    display.println("OK");
  } else {
    display.println("None");
  }

  display.display();
}


// ======================================================
// Serial Monitor output
// ======================================================

void printGPSDataToSerial() {
  Serial.println("--------------------------------");

  if (gps.location.isValid()) {
    Serial.print("Latitude:  ");
    Serial.println(gps.location.lat(), 6);

    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
  } else {
    Serial.println("Location: No valid fix");
  }

  Serial.print("Satellites: ");

  if (gps.satellites.isValid()) {
    Serial.println(gps.satellites.value());
  } else {
    Serial.println("Invalid");
  }

  Serial.print("SD card: ");
  Serial.println(sdReady ? "OK" : "ERROR");
}