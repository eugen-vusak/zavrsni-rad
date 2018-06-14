#include <MPU_6050.h>
#include <Wire.h>

// define pins used
#define INDICATOR_LED_PIN 13
#define BUTTON_PIN 4

// all times are in milliseconds
#define SAMPLE_FREQ 50  //frequency of sampling (how many samples per second)
#define AVERAGE_PROCESS_TIME 2  //how much in average does it take to process all data

// dalay between reading with average process time taken in account
#define SAMPLE_DELAY 1000/SAMPLE_FREQ - AVERAGE_PROCESS_TIME //

// raw data read from sensor
Data data;
// data that has been smoothed out
Data smoothData(0, 0, 0, 0, 0, 0);
// amount of smoothing (default 10)
float smoothStrength = 10;

// I2C address of the MPU-6050
const int MPU_addr = 0x68;
//sensor MPU_6050
MPU_6050 mpu(MPU_addr);

int ledState = LOW;

int deviceActive = 1;        // the state

int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 20;    // the debounce time; increase if the output flickers

void setup() {

  mpu.wakeUp();
  mpu.setAccelRange(2);      // sets accelerometers range to +-2G
  mpu.setGyroRange(1000);    // sets gyroscopes range to +-1000 °/s

  startIndicatorLEDInterrupt();

  Serial.begin(115200);

  pinMode(INDICATOR_LED_PIN, OUTPUT);
  digitalWrite(INDICATOR_LED_PIN, ledState);

  //read some data at first to debounce starting data
  for (int i = 0; i < 100; i++) {
    data = mpu.measure();
    smoothData = smoothOut(data);
  }

  Serial.println("Device is ready");
}

ISR(TIMER1_COMPA_vect) { //timer1 interrupt 10Hz toggles pin 13 (LED)
  toggleLED();
}

void loop() {

  int reading = digitalRead(BUTTON_PIN);
  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // and finally if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;


      buttonState = digitalRead(BUTTON_PIN);

      // if button is pressed just toggle activity of device
      if (buttonState == HIGH) {
        toggleDeviceActive();
      }
    }
  }

  // if device is active measure data from sensor
  // smooth it out with filter
  // and send it to serial port
  if (deviceActive) {
    data = mpu.measure();
    smoothData = smoothOut(data);
    Serial.println(smoothData.toString());
    delay(SAMPLE_DELAY);      // wait for time required for desired sampling frequency
  }

  lastButtonState = reading;
}

// smooths out data
// last + [(raw - last) / smoothStrength]

// y[n] = y[n-1] + [( x[n] - y[n] ) / C )]
// is sama as
// y[n] = A * x[n] + (1 - A) y[n - 1]    where A = 1/C

Data smoothOut(Data raw) {
  return smoothData.add(raw.sub(smoothData).div(smoothStrength));
}

//toggles LED from ON to OFF and vice versa
void toggleLED() {
  ledState = ! ledState;
  digitalWrite(INDICATOR_LED_PIN, ledState);
}

//toggles device from ON to OFF and vice versa
void toggleDeviceActive() {
  deviceActive = ! deviceActive;
  digitalWrite(INDICATOR_LED_PIN, LOW);
  if (deviceActive) {
    Serial.println("Device is ready");
    startIndicatorLEDInterrupt();
  }
  else {
    stopIndicatorLEDInterrupt();
  }
}

//stops interrupt for INDICATOR_LED
void stopIndicatorLEDInterrupt() {
  TCCR1B = 0;
  TIMSK1 |= (0 << OCIE1A);
}

//starts interrupt for INDICATOR_LED
void startIndicatorLEDInterrupt() {
  cli();//stop interrupts

  //set timer1 interrupt at 10Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 10Hz increments
  OCR1A = 24999;// = (16*10^6) / (10*64) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS11 and CS10 bits for 64 prescaler
  TCCR1B |= (1 << CS11) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  sei(); // allow interrupts
}
