

#include <Arduino.h> 

#ifndef message_h // Basically, this prevents problems if someone accidently #include's the library twice.
#define message_h // starting .h




#endif




class esp8266
{
  public:
  
    esp8266(HardwareSerial *serialPort);
    
    char* getSSID();
    char* getPassWord();
    char* getHost();
    char* getUrl();
    
    float getIAQ_ppm();
    float getTemp();
    float getHumidity();
    float getEquivCO2();
    float getTvoc();
    float getParticulates();
    

    boolean getConfigVars();
    boolean getSensorVals();
    
    
 private:
  
   //---fields--//
   
    HardwareSerial *serial;
    //config fields///
    char ssid[50];
    char password[50];
    char host[50];
    char url[50];
    //sensor data fields//
    float IAQ_ppm;
    float trh_temp;
    float trh_humidity;
    float equiv_CO2;
    float tvoc;
    float particulates;
    
    //---functions---//
    void parseConfig(char*, int);
    void parseSensorVals(char* inData, int dataLength);
    

    



    





    
    
};
