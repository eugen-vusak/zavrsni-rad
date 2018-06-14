#include <MPU_6050.h>
#include <Wire.h>

// all times are in milliseconds
#define SAMPLE_FREQ 200  //frequency of sampling (how many samples per second)
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

void setup() {

  mpu.wakeUp();
  mpu.setAccelRange(2);      // sets accelerometers range to +-2G
  mpu.setGyroRange(1000);    // sets gyroscopes range to +-1000 °/s

  Serial.begin(115200);

  //read some data at first to debounce starting data
  for (int i = 0; i < 100; i++) {
    data = mpu.measure();
    smoothData = smoothOut(data);
  }
}

void loop() {
  data = mpu.measure();
  smoothData = smoothOut(data);
  Serial.print(smoothData.get_az());
  Serial.print(",");
  Serial.println(data.get_az());
  delay(SAMPLE_DELAY);      // wait for time required for desired sampling frequency
}

// smooths out data
// last + [(raw - last) / smoothStrength]

// y[n] = y[n-1] + [( x[n] - y[n] ) / C )]
// is sama as
// y[n] = A * x[n] + (1 - A) y[n - 1]    where A = 1/C

Data smoothOut(Data raw) {
  return smoothData.add(raw.sub(smoothData).div(smoothStrength));
}

