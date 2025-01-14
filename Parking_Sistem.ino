#include <Wire.h>
#define echoPin 2              
#define trigPin 4        
#define bippin 18       
long duration, distance;

void bipping(int pin, int duration) {
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(bippin, OUTPUT);
}

void loop() {
  // Măsurare distanță
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration / 58.2;

  if (distance > 60) {
    Serial.println("out of range");
  } else {
    
    Serial.println(distance);
    
    
    if (distance > 0 && distance <= 55) { 
      int interval; 

      if (distance > 30) 
      {
        interval = map(distance, 30, 55, 700, 1500); 
      } else 
      {
        interval = map(distance, 1, 30, 30, 600); 
      }

      bipping(bippin, 150); 
      delay(interval);      

    } else 
    {
      delay(1000); 
    }
  }
}
