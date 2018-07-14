#include <SoftwareSerial.h>

const int rxpin = 2;
const int txpin = 3;
int checkSerial = 0;
char k = 'L';
SoftwareSerial bluetooth(rxpin, txpin);

void setup()
{
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);
  bluetooth.begin(9600);
}

void loop()
{
  if( checkSerial == 0){
    digitalWrite(4, HIGH);
    delay(1000);
    digitalWrite(4, LOW);
    checkSerial++;
  }
  
  if(bluetooth.available()){
    k = bluetooth.read();
  }
  if( k == 'H' ){
    digitalWrite(7, HIGH);
  }
  else if (k == 'L')  {
    digitalWrite(7, LOW);
  }
   delay(10);
}
