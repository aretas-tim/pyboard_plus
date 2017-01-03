/* This Class contains functions that receive config variables and sensor data from the pyboard.*
 *  It contains functions that parse this data and save it to its respective data fields.       */



#include "esp8266.h"


esp8266::esp8266(HardwareSerial *serialPort){

    serial = serialPort;
    
    IAQ_ppm =0.0;
    trh_temp=0.0;
    trh_humidity=0.0;
    equiv_CO2=0.0;
    tvoc=0.0;
    particulates=0.0;
    
    

    
}


/*  This function reads the serial bus and receives the config variables from the 
 *  micropy board to connect to wifi. It calls parseConfig() on the data it receives 
 *  to seperate the values and stores them in the esp8266 objects private feilds.
 *  Returns True if parseConfig() doesn't throw any errors
 */
boolean esp8266::getConfigVars(){
   
    char inData[70];
    int index = 0;
    boolean gotVars = false;

    while(serial->available() > 0)
    {
         char aChar = serial->read();
         
         if(aChar == '\n')// the '\n' character is the current line delimeter
         {
              inData[index] = aChar;
              index++;
              inData[index] = '\0'; // Keep the string NULL terminated
      
              /*for debugging*/
              /*serial->println("Input array is:");
              serial->println(inData);
              serial->println("Number of bytes long is:");
              serial->println(index);*/
      
              parseConfig(inData,index); //might need (index+1) for null character
              gotVars = true;  
      
              index = 0;
              inData[index] = '\0';
              
         }else
         {
              inData[index] = aChar;
              index++;
              inData[index] = '\0'; // Keep the string NULL terminated
         }

    }//while serial.available

    return gotVars;
  
}


  
/* This function parses the data it receives. The data looks like "ssid,password,host,url\n".
 *  It seperates the values and stores them in the esp8266 objects private feilds.
 */
 
void esp8266::parseConfig(char* inData, int dataLength){
  
  

    char* p;
    int index = 0;
    char* token_array[4];

    /*For debugging*/
    //strncpy(unParsedData,inData,dataLength);//
    /*serial->println("unparsed data is: ");
    serial->println(inData);*/
   
  
    p = strtok(inData, ",\n"); //breaks the inData string at every ',' and '\n'
    token_array[index] = p; //save the substring in a token array
    index++;
    
    //Continue parsing inData untill all the tokens have been
    //saved into the token array
    while (p != '\0') 
    { //not equal to NULL
      
     
      p = strtok('\0', ",\n");  // strtok() expects NULL if we want to tokenize the same string again
      token_array[index] = p;
      index++;
  
      
    }
    
    strcpy(ssid,token_array[0]);
    strcpy(password,token_array[1]);
    strcpy(host,token_array[2]);
    strcpy(url,token_array[3]);

         /*For Debugging*/
         /* serial->println("inside parseConfig:");
          serial->println("ssid is: ");
          serial->println(ssid);
          serial->println("password is : ");
          serial->println(password);
          serial->println("host is: ");
          serial->println(host);
          serial->println("url is: ");
          serial->println(url);*/

}

/* This function reads the serial bus and receives the sensor data from the 
 *  micropy board. It calls parseSensorVals() on the data it receives 
 *  to seperate the values and stores them in the esp8266 objects private feilds.
 *  The sensr data currently comes in the form "IAQ_ppm,trh_temp,trh_humidity, equiv_co2, tvoc, particulates\n"
 */
  boolean esp8266::getSensorVals(){
    
   char inData[70];
   int index = 0;
   boolean gotVals = false;

   while(serial->available() > 0)
   {
    
     char aChar = serial->read();
     
     if(aChar == '\n')// this will be changed to '\n' for real life
     {
        inData[index] = aChar;
        index++;
        inData[index] = '\0'; // Keep the string NULL terminated

        /*For Debugging*/
        /*serial->println("Input array is:");
        serial->println(inData);
        serial->println("Number of bytes long is:");
        serial->println(index);*/

        parseSensorVals(inData,index); //might need (index+1) for null character
        gotVals = true;  

        index = 0;
        inData[index] = '\0';
     }else
     {
        inData[index] = aChar;
        index++;
        inData[index] = '\0'; // Keep the string NULL terminated
     }

    }//while serial.available

   return gotVals;
  
  }
  
/* This function parses the data it receives. The data looks like: 
 *  "IAQ_ppm,trh_temp,trh_humidity, equiv_co2, tvoc, particulates\n".
 *  It seperates the values and stores them in the esp8266 objects private feilds.
 */
 
void esp8266::parseSensorVals(char* inData, int dataLength){
  
  

  char* p;
  int index = 0;
  char* token_array[7];
  
  
  /*For Debugging*/
  //strncpy(unParsedData,inData,dataLength);//
  /*serial->println("unparsed data is: ");
  serial->println(inData);*/
 

  p = strtok(inData, ",\n"); //2nd argument is a char[] of delimiters
  token_array[index] = p;
  index++;
  
  //Continue parsing inData untill all the tokens have been
  //saved into the token array
  while (p != '\0') 
  { //not equal to NULL
    
   
    p = strtok('\0', ",\n");  //strtok() expects NULL for string on subsequent calls
    token_array[index] = p;
    index++;

    
  }
  
  IAQ_ppm = ((float) atof(token_array[0]));
  trh_temp = ((float) atof(token_array[1]));
  trh_humidity = ((float) atof(token_array[2]));
  equiv_CO2 = ((float) atof(token_array[3]));
  tvoc = ((float) atof(token_array[4]));
  particulates = ((float) atof(token_array[5]));

    
    /*strcpy(IAQ_ppm,token_array[0]);
    strcpy(trh_temp,token_array[1]);
    strcpy(trh_humidity,token_array[2]);
    strcpy(equiv_CO2,token_array[3]);
    strcpy(tvoc,token_array[4]);
    strcpy(particulates,token_array[5]);*/

    /*For Debugging*/
    /*serial->println("IAQ_PPM: ");
    serial->println(IAQ_ppm);
    serial->println("temp: ");
    serial->println(trh_temp);
    serial->println("humidity: ");
    serial->println(trh_humidity);
    serial->println("equiv C02: ");
    serial->println(equiv_CO2);
    serial->println("tvoc: ");
    serial->println(tvoc);
    serial->println("particulates: ");
    serial->println(particulates);*/
    
    
    
} 


/* ---------Getters-------------*/
/* ---------Getters-------------*/
/* ---------Getters-------------*/



char* esp8266::getSSID(){

 return ssid;

}

char* esp8266::getPassWord(){

 return password;

}

char* esp8266::getHost(){

 return host;

}

char* esp8266::getUrl(){

 return url;

}

float esp8266::getIAQ_ppm(){

 return IAQ_ppm;

}

float esp8266::getTemp(){

 return trh_temp;

}

float esp8266::getHumidity(){

 return trh_humidity;

}

float esp8266::getEquivCO2(){

 return equiv_CO2;

}

float esp8266::getTvoc(){

 return tvoc;

}

float esp8266::getParticulates(){

 return particulates;

}









