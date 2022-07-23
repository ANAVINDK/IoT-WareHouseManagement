import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Import socket module
import socket	
import pickle	
from time import sleep	

server_hostname="mercury.local"
server_port = 1246	

MQTT_ADDRESS = '192.168.55.250'
MQTT_USER = 'anavindk'
MQTT_PASSWORD = '123456787'
MQTT_TOPIC = 'home/warehouse/smoke'
MQTT_TOPIC1 = 'home/warehouse/fire'

###############################################TCPIP SOCKETS
#packedData_sem= threading.Semaphore(1)
packedData_isupdated=0
packedData={"flame":" ",
            "smoke":" ", "count":" ","temperature":" ","list":""
            } 

def update_packedData(key,value):
 #   packedData_sem.acquire()
    packedData_isupdated=1
    packedData[key]=value
  #  packedData_sem.release()
    return True


def get_connection():
    while True:
        try :
            server_ip="192.168.55.237"
            # Create a socket object
            soc = socket.socket()	
            soc.connect((server_ip, server_port))
            break
        except Exception as e:
            print("\nUnable to get reach server")
            print(e)
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

def on_message(client, userdata, msg):
        print(msg.topic + ' ' + str(msg.payload))
        if(msg.topic==MQTT_TOPIC):
            update_packedData("smoke",msg.payload)
        if(msg.topic==MQTT_TOPIC1):
            update_packedData("fire",msg.payload)
        
        sendData_tcp(SOC,packedData)
        
            
# print(msg.topic + ' ' + str(msg.payload))
#print(msg.payload)
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
        if msg.payload < 25:
                GPIO.output(10, GPIO.HIGH)
               
        else:
                GPIO.output(12, GPIO.HIGH)
                
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




