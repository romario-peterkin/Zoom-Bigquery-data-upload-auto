import http.client
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

def get_all_phone_users(token):

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/phone/users", headers=headers)

    res = conn.getresponse()
    data = res.read()

    all_phone_users = json.loads(data.decode("utf-8"))
    print(all_phone_users['total_records'])


    with open('zoom_phone_users.jsonl', 'w') as outfile:
        for entry in all_phone_users['users']:
            json.dump(entry, outfile)
            outfile.write('\n')



    print("List of Zoom Phone numbers compiled to zoom_phone_users.jsonl")
