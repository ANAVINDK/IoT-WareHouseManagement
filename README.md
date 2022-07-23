# IoT-WareHouseManagement

## Microcontroller Boards
1. LPC2148
2. Arduino
3. Node MCU
4. Raspberry Pi

## Sensors

1. Temperature - LM35
2. Smoke Sensor - MQ 2
3. Fire Sensor
4. RFID reader & tag 
5. IR sensor

## Communication Technologies(Protocols)

1. Zigbee -(UART protocol)
2. WiFi -  (MQTT protocol)
3. NRF  -  (SPI Protocol) 

## Descriptions
This project implements a warehouse management system which monitors the temperature ,presence of fire and smoke conditions in a warehouse and displays the list of goods of warehouse in a custom user interface (GUI). This also counts the number of workers present inside the warehouse .  System consists of three sensor nodes measuring temperature , sensing smoke  and fire, and counting humans . The goods list are updated using RFID reader. whenever a new item is added its RFID tag is scanned and updated. All sensor data are sent to a gateway(raspberry Pi) and stored in a database. From this database, data is sent to local server using TCP-IP connection. The data are then evaluated and displayed in GUI in laptop. GUI consists of a temperature graph , stock list , Human count.
