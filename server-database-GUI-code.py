import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Import socket module
import socket	
import pickle	
from time import sleep     #import time library
import serial
import string

import spidev
from lib_nrf24 import NRF24   #import NRF24 library

GPIO.setmode(GPIO.BCM) 


server_hostname="mercury.local"
server_port = 1246	

MQTT_ADDRESS = '192.168.192.250'
MQTT_USER = 'anavindk'
MQTT_PASSWORD = '123456787'
MQTT_TOPIC =  'home/warehouse/smoke'
MQTT_TOPIC1 = 'home/warehouse/fire'
MQTT_TOPIC2 = 'home/warehouse/TabletCount'
MQTT_TOPIC3 = 'home/warehouse/LaptopCount'
MQTT_TOPIC4 = 'home/warehouse/AndroidPhoneCount'

###############################################TCPIP SOCKETS
#packedData_sem= threading.Semaphore(1)

packedData_isupdated=0
packedData={"count":0,"temperature":0.00,"TabletCount":"0","AndroidPhoneCount":0,"LaptopCount":0,"smoke":0,"flame":0}

#zigbee code
ser = serial.Serial(port='/dev/ttyUSB0',
                    
                    baudrate =9600,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout =1
                    )



        #nrf  code

pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins

radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25

radio.setPayloadSize(32)  #set the payload size as 32 bytes

radio.setChannel(0x65) # set the channel as 76 hex

radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate

radio.setPALevel(NRF24.PA_MIN)  # set PA level


radio.setAutoAck(True)       # set acknowledgement as true 

radio.enableDynamicPayloads()

radio.enableAckPayload()


radio.openReadingPipe(1, pipes[0])     # open the defined pipe for writing

radio.printDetails()      # print basic detals of radio

radio.startListening()




def update_packedData(key,value):
 #   packedData_sem.acquire()
    packedData_isupdated=1
    packedData[key]=value
  #  packedData_sem.release()
    return True
#loooopppp for every sensor



def get_connection():
    while True:
        try :
            server_ip="192.168.192.237"
            # Create a socket object
            soc = socket.socket()	
            soc.connect((server_ip, server_port))
            break
        except Exception as e:
            print("\nUnable to get reach server")
            sleep(2)
    
    return soc

SOC=get_connection()


def sendData_tcp(sock,DATA):
    data=pickle.dumps(DATA)
    try:
        sock.send(data)
        return True
    except Exception as e:
        print(Fore.RED,e,Fore.RESET)
        return False


#############################################


def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe(MQTT_TOPIC)
        client.subscribe(MQTT_TOPIC1)
        client.subscribe(MQTT_TOPIC2)
        client.subscribe(MQTT_TOPIC3)
        client.subscribe(MQTT_TOPIC4)

def on_message(client, userdata, msg):
        print(msg.topic + ' ' + str(msg.payload))
        if(msg.topic == MQTT_TOPIC):
            update_packedData("smoke",msg.payload)
        if(msg.topic==MQTT_TOPIC1):
            update_packedData("flame",msg.payload)
        if(msg.topic==MQTT_TOPIC2):
            update_packedData("TabletCount",msg.payload)
        if(msg.topic==MQTT_TOPIC3):
            update_packedData("LaptopCount",msg.payload)    
        if(msg.topic==MQTT_TOPIC4):
            update_packedData("AndroidPhoneCount",msg.payload)
        try :
            sval =ser.readline(4)
            temperature = float(sval)/100
            update_packedData("temperature",temperature)
        except :
            pass
                 
                 
        if radio.available(0):
            sleep(1/100)
        receivedMessage=[]
    #message_lis=[]
    #data=str(ser.readline())
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        
        update_packedData("count",receivedMessage[0])
        print(receivedMessage[0])
        sendData_tcp(SOC,packedData)
        print(packedData)     
        
            
# print(msg.topic + ' ' + str(msg.payload))
#print(msg.payload)
        GPIO.setwarnings(False) # Ignore warning for now
        
                
def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()
    
        
        
    

        
        
        



if __name__ == '__main__':
      print('MQTT to InfluxDB bridge')
      main()






