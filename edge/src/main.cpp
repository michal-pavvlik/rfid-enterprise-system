#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 5
#define GREEN_LED_PIN 3
#define RED_LED_PIN 2

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);

  Serial.println("Tap RFID/NFC Tag on reader");
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      // Serial.print("RFID/NFC Tag Type: ");
      // Serial.println(rfid.PICC_GetTypeName(piccType));

      // print NUID in Serial Monitor in the hex format
      String scanned_uid = "";
      String pass_uid = "adb3393";
      //for (int i = 0; i < rfid.uid.size; i++) {
        //Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
        //Serial.print(rfid.uid.uidByte[i], HEX);

        //digitalWrite(GREEN_LED_PIN, HIGH);
      //}
      for (int i = 0; i < rfid.uid.size; i++){
        scanned_uid += String(rfid.uid.uidByte[i], HEX);
      }

      if(scanned_uid == pass_uid){
        digitalWrite(GREEN_LED_PIN, HIGH);
        delay(1000);
        digitalWrite(GREEN_LED_PIN, LOW);
      }
      if(scanned_uid != pass_uid){
        digitalWrite(RED_LED_PIN, HIGH);
        delay(1000);
        digitalWrite(RED_LED_PIN, LOW);
      }

      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
    }
  }
}