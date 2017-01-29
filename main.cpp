#include "libraries.h"

/*
CHRISTMAS BREAK GOALS: 
1) Get major communications hardware working
	a) Serial (put the ring buffer inside class)	COMPLETE
	b) I2C & SPI (test with sensors)

2) ADC
	a) Goal is to create a FFT algorithm using the ADC
	
3) Accurate blocking delay functions
	a) Seconds
	b) Milliseconds	(COMPLETE)
	c) Microseconds 
	d) Nanoseconds

4) Accurate time elapsed since program start -> floating point option??
	a) Seconds
	b) Milliseconds	(COMPLETE)
	c) Microseconds
	d) Nanoseconds 
*/
#define debugPin1	23
#define debugPin2	25

//Telemetry SPI setup info
#define XM_CS		52		//Chip select
#define XM_CH		0		//Spi channel
#define GYRO_CS		53		//Chip select
#define GYRO_CH		1		//Spi channel
#define CONFIG		(SPI_CSR_BITS_16_BIT | SPI_CSR_NCPHA)

LSM9DS0 LSM = LSM9DS0(&SPI, CONFIG, XM_CH, XM_CS, GYRO_CH, GYRO_CS);
VCNL4010 PROX = VCNL4010(&Wire);


void testFunc(){
	
	Serial.write(0x00F1,_16BIT);
	Serial.write(0x3132,_16BIT);
	Serial.write(0x2E33,_16BIT);
	Serial.write(0x3435,_16BIT);
	Serial.write(0x3637,_16BIT);
	Serial.write(0x2020,_16BIT);
	Serial.write(0xFF55,_16BIT);
	/*
	Serial.write(0x00C7,_16BIT);
	Serial.write(0x3133,_16BIT);
	Serial.write(0x2E35,_16BIT);
	Serial.write(0x3739,_16BIT);
	Serial.write(0x3234,_16BIT);
	Serial.write(0x2020,_16BIT);
	Serial.write(0xFFAA,_16BIT);
	*/
	
/*
	Serial.write(0x01,_16BIT);		// Head (SOH)
	Serial.write(0xEFFA,_16BIT);	// X
	Serial.write(0xBDFF,_16BIT);	// Y
	Serial.write(0xF03F,_16BIT);	// Z
	Serial.write(0x03,_16BIT);		// End of Text (ETX)
*/

	// start=00, message=C5 (acc_y), "12.3456   ", stop=255
	
	//Write 1
	//Wire.beginTransmission(0x13);
	///Wire.write(0x87);
	//Wire.endTransmission();

	//Wire.requestFrom(0x13, 1);
	
	//Write 2
// 	Wire.beginTransmission(0x13);
// 	Wire.write(0x87);
// 	Wire.endTransmission();
// 
// 	Wire.requestFrom(0x13, 1);
	
	//PROX.readProximity();
	taskList.schedule(testFunc, 500);
}


int main(void)
{
    /* Initialize the SAM system */
    SystemInit();
	
	//Setup the debug pins
	pinMode(debugPin1, OUTPUT);
	pinMode(debugPin2, OUTPUT);
	digitalWrite(debugPin1, HIGH);
	digitalWrite(debugPin2, HIGH);

	
	Serial1.begin();
	Wire.begin();
	
	Serial.begin();
	//PROX.begin();
	//testCapture.begin();
	
	/*
	LSM.begin(GYROSCALE_245DPS, ACCELRANGE_2G, MAGGAIN_2GAUSS,
				GYRO_ODR_190_BW_125, ACCELDATARATE_100HZ, MAGDATARATE_50HZ);
	
	LSM.calibrateLSM9DS0();
	*/
	
	testFunc();
	
	
	//Delay a bit to let setup settle.
	delayMilliseconds(500);
	
    while (1) 
    {
		taskList.update(); //Check if any functions are scheduled to run
		//^^^ Expand this to include the ability to call more than void(*)(void) functions
		
		
		//Sign of life
		digitalWrite(debugPin1, HIGH);
		digitalWrite(debugPin1, LOW);
    }
}


/*
Major Hardware Areas to Develop:
-PIO Controller
-SPI Interface
-Two-Wire Interface (I2C)
-UART  (Serial)						COMPLETE
-USART (Serial)						COMPLETE
-Timer Counter
-Analog to Digital Converter (ADC)
-Digital to Analog Converter (DAC)
-PWM Generation
-CAN Bus
-True Random Number Generator
*/