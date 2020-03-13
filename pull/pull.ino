#include <SPI.h>
#include <SD.h>
File root;
void setup() {
    Serial.begin(9600);
    while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    }
    Serial.print("Initializing SD card...");
    
    if (!SD.begin(4)) {
       Serial.println("initialization failed!");
       while(1);
    }
    Serial.println("initialization done.");
}

void sendFiles(){
    root = SD.open("/");
    while (true)
    {
      File e = root.openNextFile();
      if(!e){
        // no more files
        break;
      }
      if (! e.isDirectory()){
        String filename = e.name();
        int len = filename.length();
        //if (filename.substring(len-4, len-1) == "CSV"){
          Serial.println(e.name());
          while(e.available()){
            Serial.write(e.read());
          }
          e.close();
          Serial.println('\n');
        //}
      }
    }
}
 
void loop() {
 int activate = -1;
 while (activate == -1){
  activate = Serial.read();
  }
  sendFiles();
}
