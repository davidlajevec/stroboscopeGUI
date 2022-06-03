char userInput;
int nPulses = 1;
int PulseWidthMicro = 100;
int PulseWidthNano = 0;
int InterPulseWidthMicro = 100;
int InterPulseWidthNano = 0;
float Scale1st = 1.00;

const int pinCamera = 7; //input pin for trigger from camera
const int pinLED = 2;  //pin with led 

int pinCamera1 = 0; 
int pinCamera2 = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  //pinMode(pinLED, OUTPUT);
  //pinMode(pinCamera, INPUT);
}

void getUserData() { 
  String userDataString;
  userDataString = Serial.readString();
  
  int a = userDataString.charAt(0) - '0'; 
  int b = userDataString.charAt(1) - '0';
  int c = userDataString.charAt(2) - '0';
  int d = userDataString.charAt(3) - '0';
  int e = userDataString.charAt(4) - '0';
  int f = userDataString.charAt(5) - '0';
  int g = userDataString.charAt(6) - '0';
  int h = userDataString.charAt(7) - '0';
  int i = userDataString.charAt(8) - '0';
  int j = userDataString.charAt(9) - '0';
  int k = userDataString.charAt(10) - '0';
  int l = userDataString.charAt(11) - '0';
  int m = userDataString.charAt(12) - '0';
  int n = userDataString.charAt(13) - '0';
  int o = userDataString.charAt(14) - '0';
  int p = userDataString.charAt(15) - '0';
  
  nPulses = a*10+b;
  PulseWidthMicro = c*100+d*10+e;
  PulseWidthNano = f*10+g;
  InterPulseWidthMicro = h*100+i*10+j;
  InterPulseWidthNano = k*10+l; 
  Scale1st = m*10+n+o*0.1+p*0.01;
} // getUserData Function

void loop() {
//pinCamera1 = digitalRead(pinCamera);
//if (pinCamera1>pinCamera2) LED_start();
//pinCamera2=pinCamera1;
//if (Serial.available() > 0) getUserData();
LED_start();
if (Serial.available() > 0) getUserData();
}

void LED_start() {
  for (int count = 0; count < nPulses; count++)  {
    //digitalWrite(pinLED, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    delayMicroseconds(PulseWidthMicro);
    //delayNanoseconds(PulseWidthNano);
    //digitalWrite(pinLED, LOW);
    if (count == 0){
    digitalWrite(LED_BUILTIN, LOW);
    delay(InterPulseWidthMicro*Scale1st);
    //delay(InterPulseWidthNano*Scale1st);
    }//if
    else{
    digitalWrite(LED_BUILTIN, LOW);
    delay(InterPulseWidthMicro);
    //delay(InterPulseWidthNano);}
    }//else
  } // for
} // void LED_start
