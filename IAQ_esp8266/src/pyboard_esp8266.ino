
     
#include <ESP8266WiFi.h>
#include "esp8266.h"

///global variables///
esp8266 thisBoard = esp8266(&Serial);
unsigned long prevSensorMillis = 0;
unsigned long prevServerMillis = 0;
unsigned long sensorInterval = 10000;
unsigned long serverInterval = 20000;
WiFiClient client;
const int httpPort = 80;

   
     
  void setup(){
    
        
      Serial.begin(115200);
      delay(1000);
         
      //////get ssid, passowrd and host from pyboard//////////////////
      // This loop wont exit until the pyboard has sent the config variables
      while(!(thisBoard.getConfigVars()))///while config vars have not been recieved
      { 
       
          Serial.println("configuring");
          delay(500);
      
      }
      Serial.println("____________________");
      //Connect to the Wifi Network///////  
      WiFi.begin(thisBoard.getSSID(), thisBoard.getPassWord());
      
      //while the wifi status is not connected
      while (WiFi.status() != WL_CONNECTED)
      {
          delay(500);
          Serial.print(".");
      }
     
      Serial.println("");
      Serial.println("WiFi connected");  
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
  
      delay(5000);
  
  
      Serial.print("connecting to ");
      Serial.println(thisBoard.getHost());
      
     //pyBoard looks for below statement to begin sending sensor data
      Serial.println("done configuring");  
           
  }//setup()
     
    
     
  void loop() {

       /* should the pyboard reset for some reason, might want to write some code that periodically looks for
          the config vars being sent on the serial bus.*/
       
       delay(1000);
       unsigned long currentMillis = millis();

       //////////// if the Sensor Interval has been exceed get sensor values from the pyboard //////////////
       if((currentMillis - prevSensorMillis > sensorInterval)||(prevSensorMillis == 0)) 
       {
             
              // save the last time write occured 
              prevSensorMillis = currentMillis; 
              thisBoard.getSensorVals();
           
       }
       
   
      /// If server interval has been exceeded report sensor data to the web server
      if(currentMillis - prevServerMillis > serverInterval||(prevServerMillis == 0)) 
      {
          prevServerMillis = currentMillis; 
     
          /////// if WiFi connection is broken reconnect /////////////
          if(WiFi.status()!=WL_CONNECTED){
  
              WiFi.begin(thisBoard.getSSID(), thisBoard.getPassWord());
              Serial.println("WiFi not connected, attempting to reconnect");
              while (WiFi.status() != WL_CONNECTED)///stay in loop until reconnected to WiFi
              {
                  delay(500);
                  Serial.print(".");
              }
          }
        
            ///////// connect to client and write data then close the conection ///////////////
          if(!client.connected())
          {
    
              if (!client.connect(thisBoard.getHost(), httpPort)) //if connection fails
              {
                    
                  delay(100);
                  Serial.println("connection failure");
                  delay(100);
                  return;
                    
              }else
              {
                     
                  delay(200);
                  Serial.println("connection success");
                  delay(100);
               }
          }
     
          // We now create a URI for the request
          //String url = "/testwifi/index.html";
          Serial.print("Requesting URL: ");
          Serial.println(thisBoard.getUrl());
            
            
           // This will send the request to the server
           client.print(String("GET ") + thisBoard.getUrl() +"?"+"IAQ_ppm="+thisBoard.getIAQ_ppm()+"&Temp="+thisBoard.getTemp()+
                   "&Humidity="+thisBoard.getHumidity()+"&EquivCO2="+thisBoard.getEquivCO2()+"&Tvoc="+thisBoard.getTvoc()+
                   "&Particulates="+thisBoard.getParticulates()+" HTTP/1.1\r\n" +
                   "Host: " + thisBoard.getHost() + "\r\n" + 
                   "Connection: close\r\n\r\n");

            delay(10);
            
            // Read all the lines of the reply from server and print them to Serial
            while(client.available())
            {
              
                String line = client.readStringUntil('\r');
                Serial.println(line);
                
            }
            
            Serial.println();
            Serial.println("closing connection");
            
      }//if server interval has been exceeded   
  
  }//end loop




 
