
#define ENABLE 2
#define DIRECTION 3
#define CLOCK 4
#define CURRENTLOW 6
#define maxCounter 440

void setup() {
  pinMode(ENABLE, OUTPUT);
  pinMode(DIRECTION, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  pinMode(CURRENTLOW, OUTPUT);

  digitalWrite(ENABLE, HIGH);
  digitalWrite(CURRENTLOW, LOW);

  Serial.begin(9600);
}

void loop() {  

  while (Serial.available() == 0)
  {}
  
  int incoming = Serial.parseInt();
 
  if(incoming > 0)
  {
    execute(LOW, incoming);
  }

  if(incoming < 0)
  {
    execute(HIGH, incoming);
  }
}

void execute(int turnDirection, int distance) 
{
  Serial.println("start turn");
  
  digitalWrite(DIRECTION, turnDirection);
  digitalWrite(ENABLE, LOW);

  int counter = 0;
  while(counter < maxCounter * abs(distance)) 
  {    
    digitalWrite(CLOCK, HIGH);   
    delay(2);                    
    digitalWrite(CLOCK, LOW);    
    delay(2);  // wait for a second

    counter++;
  }

  digitalWrite(ENABLE, HIGH);

  Serial.println("end turn");
}
