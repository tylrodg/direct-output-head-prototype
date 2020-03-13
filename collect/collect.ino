
#include <SPI.h>
#include <SD.h>

const int chipSelect = 4;
int j = 0;
String filenum;
String name_str;
unsigned long time_passed;
File root;
File data;
bool active = true;
// Make sure these two variables are correct for your setup
int scale = 200; // 3 (±3g) for ADXL337, 200 (±200g) for ADXL377
boolean micro_is_5V = false; // Set to true if using a 5V microcontroller such as the Arduino Uno, false if using a 3.3V microcontroller, this affects the interpretation of the sensor data

void setup()
{
  // Initialize serial communication at 115200 baud
  Serial.begin(115200);
  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
  root = SD.open("/");
  int numFiles = printFiles(root)+1;
  filenum = String(numFiles);
  name_str = "DATA";
  name_str+= filenum + ".csv";
  data = SD.open(name_str, FILE_WRITE);
  Serial.println(name_str);
  data.println("timestamp (ms), x (G), y (G), z (G)");
  time_passed = millis();
  
}

int printFiles(File dir)
{
  int i=0;
  while (true)
  {
    File entry =  dir.openNextFile();
    if (! entry)
    {
      break;
    }
    i++;
    entry.close();
  }
  Serial.println(String(i));
  return i;
}

// Read, scale, and print accelerometer data
void loop()
{
  while (millis()-time_passed <=15000){
    Serial.println(millis());
    // Get raw accelerometer data for each axis
    int rawX = analogRead(A0);
    int rawY = analogRead(A1);
    int rawZ = analogRead(A2);
    
    // Scale accelerometer ADC readings into common units
    float scaledX, scaledY, scaledZ; // Scaled values for each axis
    scaledX = mapf(rawX, 0, 1023, -scale, scale);
    scaledY = mapf(rawY, 0, 1023, -scale, scale);
    scaledZ = mapf(rawZ, 0, 1023, -scale, scale);
    
  
    String dataString = String(millis()) + ",";
    dataString+=String(scaledX) + ",";
    dataString+=String(scaledY) + ",";
    dataString+=String(scaledZ);
  
    data.println(dataString);
  
    delay(10); // Minimum delay of 2 milliseconds between sensor reads (500 Hz)
  }
  active = false;
  if(!active and j == 0){
    Serial.println("done");
    data.close();
    active = true;
    j++;
//    File f = SD.open(name_str);
//    while(f.available()){
//      Serial.write(f.read());
//    }
//    f.close();
    return;
  }
}

// Same functionality as Arduino's standard map function, except using floats
float mapf(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
