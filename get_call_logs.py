import http.client
import json
import ssl
import os
from datetime import datetime, timedelta


ssl._create_default_https_context = ssl._create_unverified_context

def get_call_logs(token):

    ssl._create_default_https_context = ssl._create_unverified_context
    start = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
    end = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer %s" % token,
        'content-type': "application/json"
        }
    params = "page_size=300&to="+end+"&from="+start+"&type=past"
    conn.request("GET", "/v2/phone/metrics/call_logs?"+params, headers=headers)

    res = conn.getresponse()
    print(res)

    data = res.read()

    master_call_logs_list = []

    all_call_logs = json.loads(data.decode("utf-8"))

    next_page = all_call_logs['next_page_token']

    all_call_logs = json.loads(data.decode("utf-8"))
    for j in all_call_logs['call_logs']:
    	master_call_logs_list.append(j)


    while next_page != "":
    	c = 0
    	print(len(master_call_logs_list))
    	print('SLEEPING')
    	time.sleep(15)
    	conn.request("GET", "/v2/phone/metrics/call_logs?"+next_page+"&"+params, headers=headers)

    	res = conn.getresponse()

    	data = res.read()

    	all_call_logs = json.loads(data.decode("utf-8"))


    	for j in all_call_logs['call_logs']:
    		c+=1
    		master_call_logs_list.append(j)
    	next_page = all_call_logs['next_page_token']
    	print(c)


    with open('call_logs.jsonl', 'w') as outfile:
        for entry in master_call_logs_list:
            json.dump(entry, outfile)
            outfile.write('\n')
