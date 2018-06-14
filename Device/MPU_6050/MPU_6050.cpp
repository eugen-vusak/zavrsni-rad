#include "Arduino.h"
#include "MPU_6050.h"

Data::Data()
{
	
}

Data::Data(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz)
{
  _ax = ax;
  _ay = ay;
  _az = az;
  _gx = gx;
  _gy = gy;
  _gz = gz;
}

void Data::print()
{
  Serial.print("ax = "); Serial.print(_ax);
    Serial.print(" | ay = "); Serial.print(_ay);
    Serial.print(" | az = "); Serial.print(_az);
    Serial.print(" | gx = "); Serial.print(_gx);
    Serial.print(" | gy = "); Serial.print(_gy);
    Serial.print(" | gz = "); Serial.println(_gz);
}

String Data::toString(){
	return 
		String(_ax)+","+
		String(_ay)+","+
		String(_az)+","+
		String(_gx)+","+
		String(_gy)+","+
		String(_gz);
}

Data Data::add(Data other){
	Data data(
		_ax + other._ax,
		_ay + other._ay,
		_az + other._az,
		_gx + other._gx,
		_gy + other._gy,
		_gz + other._gz
		);
	return data;
}

Data Data::sub(Data other){
	Data data(
		_ax - other._ax,
		_ay - other._ay,
		_az - other._az,
		_gx - other._gx,
		_gy - other._gy,
		_gz - other._gz
		);
	return data;
}

Data Data::div(int16_t c)
{
    Data data(
        _ax / c,
        _ay / c, 
        _az / c,
        _gx / c,
        _gy / c,
        _gz / c
        );

    return data;
}
int16_t Data::get_ax(){
	return _ax;
}
int16_t Data::get_ay(){
	return _ay;
}
int16_t Data::get_az(){
	return _az;
}
int16_t Data::get_gx(){
	return _gx;
}
int16_t Data::get_gy(){
	return _gy;
}
int16_t Data::get_gz(){
	return _gz;
}

MPU_6050::MPU_6050(int MPU_adr)
{
	 _MPU_adr = MPU_adr;
   _gyro_config_reg_add = 0x1B;
   _accel_config_reg_add = 0x1C;
}

void MPU_6050::wakeUp()
{
	Wire.begin();
	Wire.beginTransmission(_MPU_adr);
	Wire.write(0x6B);  // PWR_MGMT_1 register
	Wire.write(0);     // set to zero (wakes up the MPU-6050)
	Wire.endTransmission(true);
}

void MPU_6050::setAccelRange(int16_t range){
  char byte = 0x0;
  switch(range){
    case 2:
      //byte = 0x0;
      break;
    case 4:
      byte = 0x08;
      break;
    case 8:
      byte = 0x10;
      break;
    case 16:
      byte = 0x18;
      break;
  }

  Wire.beginTransmission(_MPU_adr);    //Start communicating with the MPU-6050
  Wire.write(_accel_config_reg_add);              //Send the requested starting register
  Wire.write(byte);              //Set the requested starting register
  Wire.endTransmission(true);         //End the transmission
}

void MPU_6050::setGyroRange(int16_t range){
  char byte = 0x0;
  switch(range){
    case 250:
      //byte = 0x0;
      break;
    case 500:
      byte = 0x08;
      break;
    case 1000:
      byte = 0x10;
      break;
    case 2000:
      byte = 0x18;
      break;
  }

  Wire.beginTransmission(_MPU_adr);    //Start communicating with the MPU-6050
  Wire.write(_gyro_config_reg_add);              //Send the requested starting register
  Wire.write(byte);              //Set the requested starting register
  Wire.endTransmission(true);         //End the transmission
}

Data MPU_6050::measure()
{
	Wire.beginTransmission(_MPU_adr);
  	Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  	Wire.endTransmission(false);
  	Wire.requestFrom(_MPU_adr, 14, true); // request a total of 14 registers
  	int16_t ax = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  	int16_t ay = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  	int16_t az = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  	int16_t Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  	int16_t gx = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  	int16_t gy = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  	int16_t gz = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  	Data data(ax,ay,az,gx,gy,gz);
    return data;
}