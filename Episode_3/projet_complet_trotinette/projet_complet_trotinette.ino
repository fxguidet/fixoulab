//fixoulab episode 3
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;

#include <SoftwareSerial.h>
#define ARDUINO_RX 5// Pin 5 de l'arduino vers le TX du MP3
#define ARDUINO_TX 6//Pin 6 vers le RX du MP3

SoftwareSerial mySerial(ARDUINO_RX, ARDUINO_TX);// Initialise le protocole serie en recupérant les pin  TX et RX.
static int8_t Send_buf[8] = {0} ;//On envoie des ordres en  8 int sur le MP3  //0X7E FF 06 command 00 00 00 EF;(if command =01 next song order) 
#define NEXT_SONG 0X01 
#define PREV_SONG 0X02 
#define CMD_PLAY_W_INDEX 0X03 //Donnée obligatoire,nombre de fichiers sur la carte SD.
#define VOLUME_UP_ONE 0X04
#define VOLUME_DOWN_ONE 0X05
#define CMD_SET_VOLUME 0X06// Donnée obligatoire, volume de sortie entre 0 et 30(0x1E)
#define SET_DAC 0X17
#define CMD_PLAY_WITHVOLUME 0X22 //data is needed  0x7E 06 22 00 xx yy EF;(xx volume)(yy number of song)
#define CMD_SEL_DEV 0X09 //SELECT STORAGE DEVICE, DATA IS REQUIRED
#define DEV_TF 0X02 //HELLO,IM THE DATA REQUIRED
#define SLEEP_MODE_START 0X0A
#define SLEEP_MODE_WAKEUP 0X0B
#define CMD_RESET 0X0C//CHIP RESET
#define CMD_PLAY 0X0D //RESUME PLAYBACK
#define CMD_PAUSE 0X0E //PLAYBACK IS PAUSED
#define CMD_PLAY_WITHFOLDER 0X0F//DATA IS NEEDED, 0x7E 06 0F 00 01 02 EF;(play the song with the directory \01\002xxxxxx.mp3
#define STOP_PLAY 0X16
#define PLAY_FOLDER 0X17// data is needed 0x7E 06 17 00 01 XX EF;(play the 01 folder)(value xx we dont care)
#define SET_CYCLEPLAY 0X19//data is needed 00 start; 01 close
#define SET_DAC 0X17//data is needed 00 start DAC OUTPUT;01 DAC no output




void setup(void) {

  Serial.begin(115200);// serie supervision
  mySerial.begin(9600);//serie vers mp3
  //while (!Serial) {
  //delay(10); // will pause Zero, Leonardo, etc until serial console opens
  //}
  if (!mpu.begin()) { // important , initialise le MPU6050 !!
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  delay(500);//Wait chip initialization is complete
  sendCommand(CMD_SEL_DEV, DEV_TF);//select the TF card  
  delay(200);//wait for 200ms
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("initialisation ok");
  delay(100);
  
  pinMode(2, INPUT_PULLUP); // activation du pin 2 pour l'interruption bouton lecture
  pinMode(3, INPUT_PULLUP); //  activation du pin 2 pour l'interruption bouton  stop 
  
  attachInterrupt(digitalPinToInterrupt(2),jouerson,FALLING);
  attachInterrupt(digitalPinToInterrupt(3),arretson,FALLING);
  
  sendCommand(CMD_SEL_DEV, DEV_TF);
}

void loop() {
   sensors_event_t a, g, temp;
   mpu.getEvent(&a, &g, &temp);
   //Serial.print(a.acceleration.y);
   //Serial.print(",");
   //Serial.print(a.acceleration.x);
   //Serial.print(",");
   //Serial.print(a.acceleration.z);
   //Serial.println("");
   //Serial.print(g.gyro.x);
   //Serial.print(",");
   //Serial.print(g.gyro.y);
   //Serial.print(",");
   //Serial.print(g.gyro.z);
   //Serial.println("");
   //Serial.println("");
   //Serial.println("");
  if (a.acceleration.y > 0) {
    Serial.println("Acceleration détectée");
    sendCommand(NEXT_SONG,0X01);
    Serial.println("son joué via la detection");
  }
  else {
    Serial.println("Acceleration non détectée");
    
  }
  delay(1000);
}

void jouerson()
{
  sendCommand(NEXT_SONG,0X01);
  Serial.println("bouton son joué");
}

void arretson()
{
  sendCommand(STOP_PLAY,0X16);
  Serial.println("bouton son  off");
}

void sendCommand(int8_t command, int16_t dat)
{
 delay(20);
 Send_buf[0] = 0x7e; //starting byte
 Send_buf[1] = 0xff; //version
 Send_buf[2] = 0x06; //the number of bytes of the command without starting byte and ending byte
 Send_buf[3] = command; //
 Send_buf[4] = 0x00;//0x00 = no feedback, 0x01 = feedback
 Send_buf[5] = (int8_t)(dat >> 8);//datah
 Send_buf[6] = (int8_t)(dat); //datal
 Send_buf[7] = 0xef; //ending byte
 for(uint8_t i=0; i<8; i++)//
 {
   mySerial.write(Send_buf[i]) ;//send bit to serial mp3
   Serial.print(Send_buf[i],HEX);//send bit to serial monitor in pc
 }
 //mySerial.println();
}
