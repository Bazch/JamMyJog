from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def display_slider(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        output = ''
        output += "<html><head><title>Barry's Hi-Fi prototype</title></head>"
        output += "<p>Request: %s</p>" % self.path
        output += "<body>"
        output += "<p><span id=\"textSliderValue\">%SLIDERVALUE%</span></p>"
        output += "<p><input type=\"range\" onchange=\"updateSliderPWM(this)\" id=\"pwmSlider\" min=\"0\" max=\"255\" value=\"%SLIDERVALUE%\" step=\"1\" class=\"slider\"></p>"
        output += "<p>Slide to adjust BPM</p>"
        output += "<script>"
        output += "document.getElementById(\"pwmSlider\").addEventListener(\"input\", function(){"
        output +=   "var sliderValue = document.getElementById(\"pwmSlider\").value;"
        output +=   "document.getElementById(\"textSliderValue\").innerHTML = sliderValue;"
        output += "});"
        output += "function updateSliderPWM(element) {"
        output +=   "var sliderValue = document.getElementById(\"pwmSlider\").value;"
        output +=   "console.log(sliderValue);"
        output +=   "var xhr = new XMLHttpRequest();"
        output +=   "xhr.open(\"POST\", \"/slider?value=\"+sliderValue, true);"
        output +=   "xhr.send(sliderValue); }"
        output += "</script>"
        output += "</body><html>"
        self.wfile.write(output.encode("utf-8"))

    def do_GET(self):

        if self.path == "/slider":
            print(self.path)
            self.display_slider()
            return
        self._set_response()
        self.wfile.write(bytes("<html><head><title>Barry's Hi-Fi prototype</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-Length'])
        print(self.rfile.read(content_length).decode("utf-8"))



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
