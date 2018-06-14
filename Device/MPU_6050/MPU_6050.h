#ifndef MPU_6050_h
#define MPU_6050_h

#include "Arduino.h"
#include <Wire.h>

class Data
{
	public:
		Data();
		Data(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz);
		void print();
		String toString();
		Data add(Data other);
		Data sub(Data other);
		Data div(int16_t c);
		int16_t get_ax();
		int16_t get_ay();
		int16_t get_az();
		int16_t get_gx();
		int16_t get_gy();
		int16_t get_gz();
	private:
		int16_t _ax;
		int16_t _ay;
		int16_t _az;
		int16_t _gx;
		int16_t _gy;
		int16_t _gz;
};

class MPU_6050
{
	public:
		MPU_6050(int MPU_adr);
		void wakeUp();
		void setAccelRange(int16_t range);
		void setGyroRange(int16_t range);
		Data measure();
	private:
		int16_t _MPU_adr;
		char _gyro_config_reg_add;
		char _accel_config_reg_add;
};

#endif