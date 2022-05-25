import sys
from flask import Flask,Response
from datetime import datetime
import requests
import time
import json 
import decimal
from decimal import Decimal
from configparser import ConfigParser
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

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
        #time.sleep(float(pollperiod))
        try:
         print(float(timeot))   
         resp=requests.get(url,verify=True,timeout=(Decimal(timeot)))
         if resp.status_code==200:
          print("Success within timeout")
          scode.append(resp.status_code)
          el.append(resp.elapsed.total_seconds())
         else:
          scode.append(404)
          el.append(0)
        except:
         scode.append(404)
         el.append(0)
         print("Status list",scode)
         print("Elapsed time list",el)
         print("Read Timeout")

        if i>int(hits):
          break  
    print("Times elapsed",el,'\t',scode)

    def events(): 
       for k in range(len(el)):
        #if el<float(pollperiod):
          yield str(d[k].split("::")[0])
          yield '\t'
         #yield str(d[k].split("::")[1])
          yield str(datetime.now().strftime("%H:%M:%S.%f")[:-3])
          yield '\t'
          #yield str(d[k].split("::")[1])
          #yield '\t'
          #yield str(scode[k])
          #yield '\t'
          #resp=requests.get(url,verify=True)
          #resp=requests.get(url,verify=True)
          #el=resp.elapsed.total_seconds()
          #for m in range(k):
          if el[k]<float(timeot) and scode[k]==200:
           print("Entries within timeout")
           yield str(scode[k])
           yield '\t'
           yield str(1000*el[k])
           yield 'ms'
          else:
           print("Entries after timeout")
           yield str(408)
           yield '\t'
           yield '--'
           #yield 'ms'
          yield '\n'
         #time.sleep(float(pollperiod))
    print(scode)
    plt.plot(scode)
    plt.show()
    print("Plot executed successfully")
    return Response(events(),content_type='application/json')
    #plt(np.array(d[0]),np.array(scode))


