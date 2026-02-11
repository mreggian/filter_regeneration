
// Author: Marina Reggiani-Guzzo
// Last modified: Feb 11, 2026
// Description: 
// 1. This script talks to a Pressure and Humidity sensor, connected to pins (rx,tx)=(2,3) and (rx,tx)=(8,9) respectively
// 2. This script saves the data, and a timestamp, to a csv file. 
// 3. Because we're using two sensors, we should inform to which one we want to communicate to this is done by specifying "P" 
// (for pressure sensor) and "H" (for humidity sensor) at the beginning of the command. For example, on the Serial Monitor: 
// > P:Cal,0
// This command will send "Cal,0" to the pressure sensor.

#include <SoftwareSerial.h>

SoftwareSerial portPressure(2,3); // rx=2, tx=3
SoftwareSerial portHumidity(8,9); // rx=8, tx=9

// Variables
String inputstring = ""; // This variable stores the command input from Serial Monitor
bool readHumidity = true; // boolean used to alternate between reading Humidity and Pressure sensors
const unsigned long interval = 3000; // alternate reading every 3 seconds
unsigned long previousMillis = 0; // start counting time=0 when script starts running

// Variables for Pressure sensor
String sensorstringPressure = ""; 
boolean sensor_string_complete_Pressure = false;

// Variables for Humidity sensor
String sensorstringHumidity = ""; 
boolean sensor_string_complete_Humidity = false;

String final_reading = "";

void setup() {
  
  // start serial ports
  Serial.begin(9600);
  portPressure.begin(9600);
  portHumidity.begin(9600);

  // set aside bytes for receiving information into these variables
  inputstring.reserve(30);
  sensorstringHumidity.reserve(30);
  sensorstringPressure.reserve(30);

  // configure pressure and humidity sensors to perform continuous readings every 3s
  portPressure.println("C,3"); 
  portHumidity.println("C,3"); 

}

void loop() {

  if (Serial.available()) {

    // This block of code deals with the commands sent by the user via Serial Monitor.
    // First, it identifies to which sensor the command should be sent to, and then it
    // sends it to the correct sensor.

    inputstring = Serial.readStringUntil(13); // collects the command, read the first 13 digits

    int index = inputstring.indexOf(':'); // identifies 
    if (index != -1) {

      String sensor = inputstring.substring(0, index);
      String command = inputstring.substring(index + 1);

      if (sensor == "P") {
        Serial.print("Sending command ");
        Serial.print(command);
        Serial.println(" to Pressure sensor.");
        portPressure.println(command);
      }
      else if (sensor == "H") {
        Serial.print("Sending command ");
        Serial.print(command);
        Serial.println(" to Humidity sensor.");
        portHumidity.println(command);
      }
    }
  }

  // === CHECK TIME === //

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis; // reset timer
    readHumidity = !readHumidity;
  }
  
  if (readHumidity) {

    // === HUMIDITY === //

    portHumidity.listen(); // make portHumidity active

    while (portHumidity.available() > 0) {
      char incharHumidity = (char)portHumidity.read(); // collects char we just received
      sensorstringHumidity += incharHumidity; // attach char to string
      if (incharHumidity == '\r') {
        sensor_string_complete_Humidity = true; // boolean indicating string is complete
      }
    }
    if (sensor_string_complete_Humidity == true) {
      if (isdigit(sensorstringHumidity[0]) == false) {
        Serial.println(sensorstringHumidity);
      }
      else {
        char sensorstring_array[30];                        
        char *HUM;                                          
        char *TMP;
        float HUM_float;                                      //float var used to hold the float value of the humidity.
        float TMP_float;                                      //float var used to hold the float value of the temperatur.
        sensorstringHumidity.toCharArray(sensorstring_array, 30);   //convert the string to a char array 
        HUM = strtok(sensorstring_array, ",");              //let's pars the array at each comma
        TMP = strtok(NULL, ",");                            //let's pars the array at each comma
        final_reading += "Humidity:";
        final_reading += HUM;
        final_reading += " | Temperature:";
        final_reading += TMP;
        //print_Humidity_data();

      }
      sensorstringHumidity = "";
      sensor_string_complete_Humidity = false;
    }
  }
  else {
    
    // === PRESSURE === //
    
    portPressure.listen(); // make portPressure active
    
    while (portPressure.available() > 0) {
      char incharPressure = (char)portPressure.read();
      sensorstringPressure += incharPressure;
      if (incharPressure == '\r') {
        sensor_string_complete_Pressure = true;
      }
      if (sensor_string_complete_Pressure == true) {
        if (isdigit(sensorstringPressure[0])) {
          final_reading += " | Pressure:";
          final_reading += sensorstringPressure;
          //Serial.println();
          //Serial.print("Pressure,");
          //Serial.print(sensorstringPressure);
          //Serial.println(",PSI");
        }
        sensorstringPressure = "";
        sensor_string_complete_Pressure = false;
        Serial.println(final_reading);
        final_reading = "";
      }
    }
  }
}

void print_Humidity_data(void) {                      //this function will pars the string  

  char sensorstring_array[30];                        //we make a char array
  char *HUM;                                          //char pointer used in string parsing.
  char *TMP;                                          //char pointer used in string parsing.
  char *NUL;                                          //char pointer used in string parsing (the sensor outputs some text that we don't need).
  char *DEW;                                          //char pointer used in string parsing.

  float HUM_float;                                      //float var used to hold the float value of the humidity.
  float TMP_float;                                      //float var used to hold the float value of the temperatur.
  float DEW_float;                                      //float var used to hold the float value of the dew point.
  
  sensorstringHumidity.toCharArray(sensorstring_array, 30);   //convert the string to a char array 
  HUM = strtok(sensorstring_array, ",");              //let's pars the array at each comma
  TMP = strtok(NULL, ",");                            //let's pars the array at each comma
  NUL = strtok(NULL, ",");                            //let's pars the array at each comma (the sensor outputs the word "DEW" in the string, we dont need it)
  DEW = strtok(NULL, ",");                            //let's pars the array at each comma

  Serial.println();                                   //this just makes the output easier to read by adding an extra blank line. 
  Serial.print("Humidity,");                               //we now print each value we parsed separately.
  Serial.println(HUM);                                //this is the humidity value.

  Serial.println();
  Serial.print("Temperature,");                           //we now print each value we parsed separately.
  Serial.print(TMP);                                //this is the air temperatur value.
  Serial.println(",C");

  //Serial.print("DEW:");                               //we now print each value we parsed separately.
  //Serial.println(DEW);                                //this is the dew point.

  //uncomment this section if you want to take the values and convert them into floating point number.
  /*
    HUM_float=atof(HUM);
    TMP_float=atof(TMP);
    DEW_float=atof(DEW);
  */
}
