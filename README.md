# IoT-WareHouseManagement
This project implements a warehouse management system which monitors the temperature ,presence of fire and smoke conditions in a warehouse and displays the list of goods of warehouse in a custom user interface (GUI). This also counts the number of workers present inside the warehouse .  System consists of three sensor nodes measuring temperature , sensing smoke  and fire, and counting humans . The goods list are updated using RFID reader. whenever a new item is added its RFID tag is scanned and updated. All sensor data are sent to a gateway(raspberry Pi) and stored in a database. From this database, data is sent to local server using TCP-IP connection. The data are then evaluated and displayed in GUI in laptop. GUI consists of a temperature graph , stock list , Human count.