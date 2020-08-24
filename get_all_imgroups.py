import http.client
import json
import ssl




def get_all_imgroups(token):


    ssl._create_default_https_context = ssl._create_unverified_context


    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/im/groups", headers=headers)

    res = conn.getresponse()
    data = res.read()

    all_imgroups = json.loads(data.decode("utf-8"))


    with open('list_of_imgroups.txt', 'w') as im_outfile:
        json.dump(all_imgroups['groups'], im_outfile)

    with open('list_of_imgroups.jsonl', 'w') as im_outfile:
        for entry in all_imgroups['groups']:
            json.dump(entry, im_outfile)
            im_outfile.write('\n')
