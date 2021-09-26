import geoip2.database
from geoip2.errors import *
from flask import Flask,request,Response,render_template
import sqlite3
import time
from datetime import datetime 

def read_Country(ip):
    with geoip2.database.Reader('geoip/GeoIP2-Country.mmdb') as reader:
        try:
            response = reader.country(ip)
            return response.country.name
        except (ValueError , AddressNotFoundError) as e:
            return None

def read_City(ip):
    with geoip2.database.Reader('geoip/GeoIP2-City.mmdb') as reader:
        try:
            response = reader.city(ip)
            return response.city.name
        except (ValueError , AddressNotFoundError) as e:
            return None

def read_ISP(ip):
    with geoip2.database.Reader('geoip/GeoIP2-ISP.mmdb') as reader:
        try:
            response = reader.isp(ip)
            return response.isp
        except (ValueError , AddressNotFoundError) as e:
            return None

def read_Domain(ip):
    with geoip2.database.Reader('geoip/GeoIP2-Domain.mmdb') as reader:
        try:
            response = reader.domain(ip)
            return response.domain
        except (ValueError , AddressNotFoundError) as e:
            return None

def handel_response(ip,ua):
    country = read_Country(ip)
    city = read_City(ip)
    isp = read_ISP(ip)
    domain = read_Domain(ip)

    conn = sqlite3.connect('database/ip_log.sqlite')
    c = conn.cursor()
    c.execute(f'''INSERT INTO ip_data(ip,time,country,city,isp,domain,user_agent) VALUES ("{ip}",{time.time()},"{country}","{city}","{isp}","{domain}","{ua}")''')
    conn.commit()
    conn.close()

    return f"{ip}\n{country}, {city}\n{isp} ({domain})"


app = Flask(__name__)

@app.route("/")
def root():
    #ip = request.environ['REMOTE_ADDR']
    ip = request.headers.get('X-Forwarded-For')
    ip = ip.split(",")[-1].strip()
    ua = request.headers.get('User-Agent')
    return Response(handel_response(ip,ua),mimetype='text/plain')

@app.route('/log')
def log():
    conn = sqlite3.connect('database/ip_log.sqlite')
    c = conn.cursor()
    cursor  = c.execute("SELECT * FROM ip_data ORDER BY ID DESC LIMIT 100")
    ret = "id\tip\t\ttime(UTC+8)\t\t\t\tcountry\t\tcity\t\tisp\t\tdomain\n"
    data = list(cursor)
    data = [list(i) for i in data]
    for i in range(len(data)):
        data[i][2] = datetime.fromtimestamp(data[i][2])
    return render_template("log.html",data=data)
