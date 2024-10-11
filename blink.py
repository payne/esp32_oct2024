import network
import socket
from machine import Pin
import time

# Wi-Fi configuration
ssid = 'YourWiFiSSID'
password = 'YourWiFiPassword'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    time.sleep(1)
print('Connected to Wi-Fi')
print('IP:', wlan.ifconfig()[0])

# Set up LED
led = Pin(2, Pin.OUT)
led_state = False

# HTML template
html = """<!DOCTYPE html>
<html>
    <body>
        <h1>ESP32 LED Control</h1>
        <p>LED is {}</p>
        <a href="/toggle"><button>Toggle LED</button></a>
    </body>
</html>
"""

# Set up web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    
    if request.find('/toggle') != -1:
        led_state = not led_state
        led.value(led_state)
    
    response = html.format("ON" if led_state else "OFF")
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()