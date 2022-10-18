#!/usr/bin/python3

# Metadata allows your plugin to show up in the app, and website.
#
#  <xbar.title>nordpool</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Fredrik Leijon</xbar.author>
#  <xbar.author.github>fredrikl</xbar.author.github>
#  <xbar.desc>Shows spotprice from nordpol.</xbar.desc>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>http://url-to-about.com/</xbar.abouturl>

from datetime import date, datetime, timedelta
from os.path import exists
import json
from locale import atof, setlocale, LC_NUMERIC
import os

# Prices is formatted for Sweden
setlocale(LC_NUMERIC, 'sv_SE')

tmpDir = os.environ['TMPDIR']
date_key = date.today().strftime("%d-%m-%Y")
file = f'{tmpDir}nordpool-{date_key}.json'

def download(date):
  import urllib
  import urllib.request
  # 29 = Sweden
  url = f'https://www.nordpoolgroup.com/api/marketdata/page/29?endDate={date}&currency=SEK'
  print("download!")
  print(url)
  result = urllib.request.urlopen(url, timeout = 10).read()
  filehandle = open(file, 'wb')
  filehandle.write(result)
  filehandle.close()


def get_hour(rows, hour):
  row = rows[hour]
  c = row['Columns'][3] # SE4 (Array goes from SE1 (0) to SE4 (3))
  value = c['Value']
  price = atof(value)
  return price /10

def show_future_prices(rows, current_hour):
    for x in range(1, 5):
      hour = current_hour +x
      if hour <= 23:
        kwh = get_hour(rows, hour)
        print(f'{hour:2.0f}-{(hour+1):2.0f}: {kwh:.2f} öre/kWh')

file_exists = exists(file)
if file_exists == False:
  download(date_key)

f = open(file)
data = json.load(f)

rows = data["data"]["Rows"]
current = datetime.now().hour
kwh = get_hour(rows, current)

print(f'⚡ {kwh:.2f} öre/kWh')
print('---')

show_future_prices(rows, current)
