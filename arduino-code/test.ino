#include <Stepper.h>
#include <Servo.h>


#define STEPS 4096
#define STEPPER_SPEED 4

#define XENDPIN 12

#define MATRIX_SIZE 12

#define SERVOPIN 7
#define ANGLE_START 180
#define ANGLE_DIP 40

#define SERIAL_SPEED 9600


Stepper stepper(STEPS, 8, 10, 9, 11);
Servo zservo;
bool t_direction = false;

void setup()
{
  // set the speed of the motor to 30 RPMs
  stepper.setSpeed(STEPPER_SPEED);
  Serial.begin(SERIAL_SPEED); 

  pinMode(XENDPIN, INPUT);
  digitalWrite(XENDPIN, HIGH);
  
  zservo.attach(SERVOPIN);
  zservo.write(ANGLE_START);

  testPT();

}

void loop()
{
  
  delay(1000);
  
  // Print out the test pattern
}

void homeX() 
{
 while(digitalRead(XENDPIN))
 {
  stepper.step(1);
 } 
  
}


void zpulse(bool p)
{
  if(p)
  {
   zservo.write(ANGLE_START);
//   delay(100);
   zservo.write(ANGLE_DIP);
   delay(1200);
   zservo.write(ANGLE_START);
  }
}

void xStep(int s)
{
  stepper.step(s*(-256-64));
}


bool xLine(unsigned long pixels, bool t_d)
{
  if (!t_d)
  {
    homeX();
    for(int flag=0; flag < MATRIX_SIZE; flag++)
    {
      xStep(1);
      // Need to mirror image
      zpulse(bitRead(pixels, MATRIX_SIZE-flag));
    } 
  }
  else 
  {
    for(int flag=MATRIX_SIZE-1; flag > -1 ; flag--)
    {
      // Need to mirror image
      zpulse(bitRead(pixels, MATRIX_SIZE-flag));
      xStep(-1);
    }     
  }
  delay(2000);
  return(!t_d);
}



/* Test

PT


011110011111  1951
010001000100  1092
010001000100  1092
010001000100  1092
011110000100  1924
010000000100  1028
010000000100  1028
010000000100  1028
010000000100  1028


*/

void testPT()
{
  t_direction = xLine(1951, t_direction);
  t_direction = xLine(1092, t_direction);
  t_direction = xLine(1092, t_direction);
  t_direction = xLine(1092, t_direction);
  t_direction = xLine(1924, t_direction);
  t_direction = xLine(1028, t_direction);
  t_direction = xLine(1028, t_direction);
  t_direction = xLine(1028, t_direction);
  t_direction = xLine(1028, t_direction);
}
