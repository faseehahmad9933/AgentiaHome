from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys
from dht import DHT11
import random
# DHT11 Sensor on Pin 4 of ESP32 (Connect DHT11 data pin to GPIO4)
dht_sensor = DHT11(Pin(34))

def randomNumber():
    sensor = random.randint(1, 98)
    return sensor

WIFI_SSID     = 'Ufone_245E9F'
WIFI_PASSWORD = 'H676u3rU'


mqtt_client_id      = bytes('client_'+'56243', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'Faseeh99'
ADAFRUIT_IO_KEY     = 'aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1'
TOGGLE_FEED_ID      = 'light'
led=Pin(2,Pin.OUT)                          # Onboard LED on Pin 2 of ESP32
# New pin for 5V output when toggle is triggered
toggle_output = Pin(26, Pin.OUT)             # Pin 5 for 5V output

TEMP_FEED_ID      = 'sensor'
FAN_FEED_ID = 'fan'  # New feed for fan toggle
fan_output = Pin(17, Pin.OUT)  # Pin 17 for fan output
DOOR_FEED_ID = 'door'  # New feed for door state
reed_sensor = Pin(16, Pin.IN, Pin.PULL_UP)  # Reed sensor on GPIO16, with pull-up

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')
        sys.exit()
        

connect_wifi() # Connecting to WiFi Router 


client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()
def cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if topic == toggle_feed:
        if recieved_data=="0":
            led.value(0)
            toggle_output.value(0)                  # Turn off 5V output
            print("Toggle OFF - 5V output disabled")
        if recieved_data=="1":
            led.value(1)
            toggle_output.value(1)                  # Turn on 5V output
            print("Toggle ON - 5V output enabled")
    elif topic == fan_feed:
        if recieved_data=="0":
            fan_output.value(0)
            print("Fan OFF - Pin 17 output disabled")
        if recieved_data=="1":
            fan_output.value(1)
            print("Fan ON - Pin 17 output enabled")
    elif topic == door_feed:
        door_state = 'closed' if recieved_data == 0 else 'open'
        print('Door state -', door_state)
        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - techiesms/feeds/temp
#hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - techiesms/feeds/hum   
toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8') # format - techiesms/feeds/led1
fan_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, FAN_FEED_ID), 'utf-8')  # format - techiesms/feeds/fan
door_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, DOOR_FEED_ID), 'utf-8')  # format - techiesms/feeds/door
client.set_callback(cb)      # Callback function               
client.subscribe(toggle_feed) 
client.subscribe(fan_feed)   # Subscribe to fan feed
client.subscribe(door_feed)  # Subscribe to door feed

def sens_data(data):
    try:
        dht_sensor.measure()                # Measuring 
        temp = dht_sensor.temperature()     # getting Temp from DHT11
    except Exception as e:
        print('DHT11 read error:', e)
        temp = randomNumber()  # fallback to random if error
    client.publish(temp_feed,
                  bytes(str(temp), 'utf-8'),   # Publishing Temp feed to adafruit.io
                  qos=0)
    print("Temperature - ", str(temp))
    # Door state logic
    door_state = 'closed' if reed_sensor.value() == 0 else 'open'  # Assuming 0 = closed
    client.publish(door_feed, bytes(door_state, 'utf-8'), qos=0)
    print('Door state -', door_state)
    print('Msg sent')
    
    
    
timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback = sens_data)
while True:
    try:
        client.check_msg()                  # non blocking function
    except :
        client.disconnect()
        sys.exit()

