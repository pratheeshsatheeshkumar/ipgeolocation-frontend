from flask import Flask, make_response, render_template, jsonify
import requests
import re
import os

app = Flask(__name__)



@app.route('/',strict_slashes=False)
@app.route('/ip',strict_slashes=False)
@app.route('/ip/<ip>',strict_slashes=False)
def index(ip=None):
  
  if ip != None:
        
    pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    valid_ip = pattern.match(ip.strip())
    
    if valid_ip:
        
      api_url = "http://{}:{}/{}/{}".format("api.pratheesh.local","80","ip",ip) 
      response = requests.get(url=api_url)
      geodata = response.json()
      container_name = geodata['container_name']
      continent_name = geodata['continent_name']
      continent_code = geodata['continent_code']
      country_name = geodata['country_name']
      isp = geodata['isp']
      cached = geodata['cached']
    
  
      return render_template('index.html',container_name=container_name,
                         continent_name=continent_name,
                         continent_code=continent_code,
                         country_name=country_name,
                         isp=isp,
                         cached=cached
                         )

    else:
        
      return render_template('error.html')

  else:
       
    return render_template('error.html')
    
@app.route('/status',strict_slashes=False)
def status():
    return make_response(jsonify(message = "Health check success!!"),200)    


if __name__ == "__main__":
    
  api_server = "api.pratheesh.local" 
  api_server_port = "80" 
  api_path = os.getenv("API_PATH",None)
  app_port = os.getenv('APP_PORT',"8080") 
  app.run(port=app_port,host="0.0.0.0",debug=True)
