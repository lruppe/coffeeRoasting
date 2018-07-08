int incomingByte = 0;   // for incoming serial data
int inByte1;
int inByte2;
int inByte3;
int power=80;
int temp=0;
int counter=0;
int counteron=1;
void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        pinMode(13,OUTPUT);
        pinMode(A0,INPUT);
        pinMode(6,OUTPUT);
}

void loop() {

        // send data only when you receive data:
        if (Serial.available() >0) {
                // read the incoming byte:
                inByte1=(Serial.read()-'0');
                delay(5);
                inByte2=(Serial.read()-'0');
                delay(5);
                inByte3=(Serial.read()-'0');
                

                if(inByte1==1){
                  power=inByte2*10+inByte3;
                  // say what you got:
                  Serial.print("I received: ");
                  Serial.print(power);
                  Serial.flush();
                }
                if(inByte1==2){
                  temp=(((analogRead(A0)*(0.0049))-1.25)/0.005)+7;
                  Serial.print(temp);
                  Serial.flush();
                  }
                if(inByte1==3){
                  counteron=1;
                  counter=0;
                }
                 if(inByte1==4){
                  Serial.print(counter);
                  Serial.flush();
                }
                
      
  }
  else{
    delay(10);}



if(counter<=power){
  digitalWrite(6,HIGH);
}
else{
    digitalWrite(6,LOW);
}
if(counter==99){
counter=0;
}
 if(counteron==1){
  counter++;
 }
  }
//  if(power!=0){
//    power+=1;
//  digitalWrite(6,HIGH);
//  delay(power*10);
//  digitalWrite(6,LOW);
//  delay(1000-power*10);
        
     
         
         
        

