import http.client
import json
import ssl


def get_all_registrants(token):


    ssl._create_default_https_context = ssl._create_unverified_context

    master_registrant_list = []



    with open('webinars.jsonl', 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        webinarId = result['id']
        topic = result['topic']
        host = result['email']
        start_time = result['start_time']
        end_time = result['end_time']
        print(str(webinarId) + ':' + topic)

        conn = http.client.HTTPSConnection("api.zoom.us")



        headers = {
            'authorization': "Bearer %s" % token ,
            'content-type': "application/json"
            }

        conn.request("GET", "/v2/webinars/%s/registrants?page_number=1&page_size=300&status=approved" % webinarId, headers=headers)

        res = conn.getresponse()
        data = res.read()


        all_data = json.loads(data.decode("utf-8"))


        page_count = all_data['page_count']


        for entry in all_data['registrants']:
            entry['webinarId'] = webinarId
            entry['topic'] = topic
            entry['host_email'] = host
            entry['start_time'] = start_time
            entry['end_time'] = end_time

        master_registrant_list += all_data['registrants']

        print('Pages: ' + str(page_count))

        i=2
        while i<page_count+1:
        	time.sleep(1)
        	print('SLEEPING: completed page ' + str(i))

        	conn.request("GET", "/v2/webinars/%s/registrants?page_number=1&page_size=30&status=approved" % webinarId, headers=headers)

        	res = conn.getresponse()

        	data = res.read()

        	all_data = json.loads(data.decode("utf-8"))

        	master_registrant_list += all_data['registrants']

        	i+=1

        print('Registrants imported.')


    with open('list_of_all_registrants.jsonl', 'w') as outfile:
        for entry in master_registrant_list:
            json.dump(entry, outfile)
            outfile.write('\n')
