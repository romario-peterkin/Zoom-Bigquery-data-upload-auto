import http.client
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

def get_all_phone_call_queues(token):

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/phone/call_queues", headers=headers)

    res = conn.getresponse()
    data = res.read()

    all_phone_call_queues = json.loads(data.decode("utf-8"))


    with open('zoom_phone_call_queues.jsonl', 'w') as outfile:
        for entry in all_phone_call_queues['call_queues']:
            json.dump(entry, outfile)
            outfile.write('\n')



    print("List of Zoom Phone numbers compiled to get_zoom_phone_call_queues.jsonl")
