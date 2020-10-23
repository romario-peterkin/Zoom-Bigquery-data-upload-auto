import http.client
import json
import time
import datetime as dt
import ssl


def get_all_participants(token):


    ssl._create_default_https_context = ssl._create_unverified_context


    with open('webinars.jsonl', 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        webinarId = result['id']
        print(webinarId)

        conn = http.client.HTTPSConnection("api.zoom.us")



        headers = {
            'authorization': "Bearer %s" % token ,
            'content-type': "application/json"
            }

        conn.request("GET", "/v2/metrics/webinars/%s/participants?page_number=1&page_size=30&type=past" % webinarId, headers=headers)

        res = conn.getresponse()
        data = res.read()

        all_data = json.loads(data.decode("utf-8"))


        page_count = all_data['page_count']
        master_participant_list = all_data['participants']


        i=2
        while i<page_count+1:
        	time.sleep(1)
        	print('SLEEPING: completed page ' + str(i))

        	conn.request("GET", "/v2/metrics/webinars/%s/participants?page_number=1&page_size=30&type=past" % webinarId, headers=headers)

        	res = conn.getresponse()

        	data = res.read()

        	all_data = json.loads(data.decode("utf-8"))


        	master_participant_list += all_data['participants']

        	i+=1





    with open('list_of_all_participants.jsonl', 'w') as outfile:
        for entry in master_participant_list:
            json.dump(entry, outfile)
            outfile.write('\n')
