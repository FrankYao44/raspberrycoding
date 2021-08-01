void attachInterrupt_fun_1(){
  Serial.println("yes yes ");
  int i;
 for(i=128;1<255;i=i+5){
  analogWrite(A1,i); 
 }
}
 void attachInterrupt_fun_2(){
  Serial.println("no no ");
 delay(500);
 while(true){
   if(digitalRead(2)){detachInterrupt(A2);
   }
 }
 }
 
 void attachInterrupt_fun_3(){
  Serial.println("oh~~~~~~~");

   int i;
 for(i=128;1>0;i=i-5){
  analogWrite(A1,i); 
 }
 
 }
 
void setup()
{
pinMode(1,OUTPUT);
pinMode(2,INPUT);
Serial.begin(9600);


  
}
void loop()
{digitalWrite(1,HIGH);

if (digitalRead(2)){
  analogWrite(A1,128);

  
}
while (  true){
 if (analogRead(A2)<255){
  attachInterrupt(A2,attachInterrupt_fun_1,FALLING);
  
  
  
 } 
   else if (analogRead(A2)>888){
  attachInterrupt(A2,attachInterrupt_fun_2,RISING);
  
  
  
 } 
 
  else{
  attachInterrupt(A2,attachInterrupt_fun_3,CHANGE);
  
  
  
 } 
}
  
  
  
}
