// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;
// defines variables
long duration;
int distance;

void setup()
{
  // Motion Sensor Variables
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);  // Sets the echoPin as an Input
  // Serial.begin(9600); // Starts the serial communication

  // DC Motor Variables
  pinMode(7, OUTPUT); // w/o wheel moto
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);

  digitalWrite(7, LOW);
  digitalWrite(6, LOW);
  digitalWrite(5, LOW);
  digitalWrite(4, LOW);

  Serial.begin(115200);
  Serial.setTimeout(5);
}

void loop()
{

  while (!Serial.available())
  {
  }

  String input = Serial.readString();
  String direction = input.substring(0, input.indexOf(","));
  String rawMoveMode = input.substring(input.indexOf(",") + 1);

  bool moveMode;
  if (rawMoveMode.equals("0"))
  {
    moveMode = false;
  }
  else
  {
    moveMode = true;
  }

  Serial.print(direction + String(moveMode) + rawMoveMode);

  // MOTION SENSOR

  // Clears the trigPin
  /*digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;*/
  // Prints the distance on the Serial Monitor
  // Serial.print("Distance: ");
  // Serial.println(distance);

  // Stop Wheels if Detect something with Motion sensor
  //  if (distance < 50 or not moveMode or direction.equals("None")){
  if (not moveMode or direction.equals("None"))
  { // delete after implementing motion thing
    digitalWrite(7, LOW);
    digitalWrite(6, LOW);
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
  }
  else
  {
    if (direction.equals("f"))
    {
      digitalWrite(7, HIGH);
      digitalWrite(6, LOW);
      digitalWrite(5, HIGH);
      digitalWrite(4, LOW);
    }
    else if (direction.equals("b"))
    {
      digitalWrite(7, LOW);
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      digitalWrite(4, HIGH);
    }
    else if (direction.equals("l"))
    {
      digitalWrite(7, HIGH);
      digitalWrite(6, LOW);
      digitalWrite(5, LOW);
      digitalWrite(4, HIGH);
    }
    else if (direction.equals("r"))
    {
      digitalWrite(7, LOW);
      digitalWrite(6, HIGH);
      digitalWrite(5, HIGH);
      digitalWrite(4, LOW);
    }
  }

  // DC MOTORS -has to be changed for adhawk + mounted movement

  // digitalWrite(7, HIGH);
  // digitalWrite(6, LOW);

  // digitalWrite(5, LOW);
  // digitalWrite(4, HIGH);

  // delay(2000);

  // digitalWrite(7, LOW);
  // digitalWrite(6, HIGH);

  // digitalWrite(5, HIGH);
  // digitalWrite(4, LOW);

  // delay(2000);
}