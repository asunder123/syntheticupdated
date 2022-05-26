import sys
from flask import Flask,Response
from datetime import datetime
import requests
import time
import json 
import decimal
from decimal import Decimal
from configparser import ConfigParser
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np
import mpld3
from flask import render_template
import io
import os
from io import BytesIO
import base64

app = Flask(__name__,template_folder='templates')

c=ConfigParser()

#Read from config file
read = c.read('config.ini')
print("Read from config file",read)

#Get endpoint from ini file
url = c.get('endpoint','url')
print("End point is ",url)

#Fetch no of hits
hits = c.get('endpoint','hits')
print("Set no of hits to ...",hits)


#sleep time
pollperiod = c.get('endpoint','pollperiod')
print("Configured poll period is....", pollperiod)

#timeout
timeot = c.get('endpoint','timeout')
print("Time out configured is ",timeot)
print(float(timeot))

@app.route("/syn")
def web():
    now = datetime.now()
    #current_time=now.strftime("%H:%M:%S")
    #resp=requests.get(url,verify=True,timeout=float(timeot))
    #print("Latency",resp.elapsed.total_seconds())
    #var=resp.text
    #status=resp.status_code
    #print("Response:::",var)
    i=0
    d=list()
    el=list()
    scode=list()
    for i in range(int(hits)):
        list_entries=str(i)+'::'+str("")
        d.append(list_entries)
        print("Entries:",d,"Type:",type(d))
        clist=d[i].split("::")
        print("Type::clist",type(clist))
        data=clist[0]+' '+clist[1]
        print("Data cleansed",data,"Type",type(data))
        time.sleep(float(pollperiod))
        try:
         print(Decimal(timeot))   
         resp=requests.get(url,verify=True,timeout=(Decimal(timeot)))
         print("Success within timeout")
         if resp.status_code==200:
          scode.append(resp.status_code)
         else:
          scode.append(408)
         el.append(resp.elapsed.total_seconds()*1000)
        except:
         print("Read Timeout")

        if i>int(hits):
          break  
    #print("Times elapsed",el,'\t',scode)

    def events(): 
       for k in range(len(el)):
        #if el<float(pollperiod):
          yield str(d[k].split("::")[0])
          yield '\t'
         #yield str(d[k].split("::")[1])
          yield str(datetime.now().strftime("%H:%M:%S.%f")[:-3])
          yield '\t'
          if el[k]<(1000*float(timeot)) and scode[k]==200:
           print("Entries within timeout")
           yield str(scode[k])
           yield '\t'
           yield str(el[k])
           yield 'ms'
          else:
           print("Entries after timeout")
           scode[k]=408
           yield str(scode[k])
           yield '\t'
           el[k]=0
           yield str(el[k])
           yield 'ms'
          yield '\n'
         #time.sleep(float(pollperiod))
       print("Status codes",scode)
       print("Readlatencies",el)
       plt.plot(np.array(scode))
       #mpld3.show()
       plt.savefig('Respcodeplot.png')
       plt.plot(np.array(el))
       #mpld3.show()
       plt.savefig('Latencyplot.png')
       print("Plot executed successfully")
    #plt.plot(np.array(el),np.array(scode))
    #plt.savefig('statuscode-resptime.png')
    return Response(events(),content_type='application/json')
    #plt(np.array(d[0]),np.array(scode))

@app.route("/plotresp")
def plotresp():
 plot_url1=  base64.b64encode(open("Respcodeplot.png","rb").read())
 plot_resp= plot_url1.decode('utf-8')
 return render_template('plotresp.html',plot_url1=plot_resp)

@app.route("/plotlat")
def plotlat():
 plot_url2=  base64.b64encode(open("Latencyplot.png","rb").read())
 plot_lat= plot_url2.decode('utf-8')
 return render_template('plotlat.html',plot_url2=plot_lat)