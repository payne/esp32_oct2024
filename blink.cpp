#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YourWiFiSSID";
const char* password = "YourWiFiPassword";

WebServer server(80);

const int led = 2;
bool ledState = LOW;

void setup() {
  Serial.begin(115200);
  pinMode(led, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/toggle", toggleLED);
  server.begin();
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 LED Control</h1>";
  html += "<p>LED is " + String(ledState ? "ON" : "OFF") + "</p>";
  html += "<a href='/toggle'><button>Toggle LED</button></a>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void toggleLED() {
  ledState = !ledState;
  digitalWrite(led, ledState);
  server.sendHeader("Location", "/");
  server.send(303);
}