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


Adafruit_LSM9DS0 LSM = Adafruit_LSM9DS0(&SPI, CONFIG, XM_CH, XM_CS, GYRO_CH, GYRO_CS);

EventCaptureClass testCapture = EventCaptureClass(7, 100000, RISING, false);
void TC7_Handler(){
	testCapture.IRQHandler();
}

void printChar(void *p, char c){
	Serial1.write((uint8_t)c, BYTE);	
}

void my_printf(const char* fmt,  ...)
{

	char buffer[150];
	va_list args;
	va_start (args, fmt);

	tfp_vsprintf(buffer, fmt, args);

	print("%s", buffer);
	va_end (args);

}

void testFunc(){
	
	
	LSM.readAccel();
	LSM.convertAccel();
	
	float varA = LSM.accelData.x;
	float varB = LSM.accelData.y;
	float varC = LSM.accelData.z;
	
	my_printf("%5.2f %5.2f %5.2f", varA, varB, varC);
	
	// Serial.write(0xFED4,_16BIT); // Dummy Data
	// Serial.write(0x0a); // Creates a newline
	// Serial.read(_16BIT);
	
	/*
	// To send real data to Linux Processor
	Serial.write(varA,_16BIT);	// X
	Serial.write(varB,_16BIT);	// Y
	Serial.write(varC,_16BIT);	// Z
	*/
	
	
	// Set 1 of Accelerometer Dummy Data
	Serial.write(0x01,_16BIT);	// Head
	Serial.write(0xEFFA,_16BIT);	// X
	Serial.write(0x0a,_16BIT); // Creates a newline
	//Serial.write(0x2C,_16BIT);			// Comma for delimiter
	Serial.write(0xBDFF,_16BIT);	// Y
	Serial.write(0x0a,_16BIT); // Creates a newline
	//Serial.write(0x2C,_16BIT);			// Comma for delimiter
	Serial.write(0xF03F,_16BIT);	// Z
	Serial.write(0x0a,_16BIT); // Creates a newline
	//Serial.write(0x2C,_16BIT);			// Comma for delimiter
	Serial.write(0x03,_16BIT);	// End of Text
	
	
	/*
	// Set 1 of Accelerometer Dummy Data
	Serial.write(0xEFFA,_16BIT);	// X
	Serial.write(0xBDFF,_16BIT);	// Y
	Serial.write(0xF03F,_16BIT);	// Z
	*/
	
	taskList.schedule(testFunc, 3);
}


int main(void)
{
    /* Initialize the SAM system */
    SystemInit();
	
	init_printf(NULL, printChar);
	
	pinMode(debugPin1, OUTPUT);
	pinMode(debugPin2, OUTPUT);
	digitalWrite(debugPin1, LOW);
	digitalWrite(debugPin2, LOW);

	
	Serial1.begin();
	testCapture.begin();
	
	Serial.begin();
	
	LSM.begin(GYROSCALE_245DPS, ACCELRANGE_2G, MAGGAIN_2GAUSS,
				GYRO_ODR_190_BW_125, ACCELDATARATE_100HZ, MAGDATARATE_50HZ);
	
	LSM.calibrateLSM9DS0();
	
	testFunc();
	
	
	
    while (1) 
    {
		taskList.update(); //Check if any functions are scheduled to run
		//^^^ Expand this to include the ability to call more than void(*)(void) functions
		
		
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