from getToken import generateToken
from get_all_users import get_all_users
from get_all_imgroups import get_all_imgroups
from get_all_meetings import get_meetings
from uploadToCloudStorage import upload_blob
from overwriteTable import overwriteBigQueryTable 
from appendTable import appendBigQueryTable 
from relate_meetings_to_projectID import get_meetings_to_projectID
import http.client
import json
import time
import datetime as dt
from datetime import timedelta
import ssl


###############
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])

##############


def uploadZoomData():

    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'World')



    bucket_name = "{ENTER_BUCKET_NAME}"
    dataset = '{ENTER_DATASET_NAME}'
    #User table configurations
    source_file_name = "{ENTER_FILENAME}"
    destination_blob_name = "{ENTER_BLOB_NAME}"
    table = '{ENTER_TABLE_NAME}'
    uri = "{ENTER_URI}"
    #IM group table configurations
    im_source_file_name = "{ENTER_FILENAME}"
    im_destination_blob_name = "{ENTER_BLOB_NAME}"
    im_table = '{ENTER_TABLE_NAME}'
    im_uri = "gs://zoom-data/list_of_imgroups.jsonl"
    #Meetings table configurations
    meetings_source_file_name = "{ENTER_FILENAME}"
    meetings_destination_blob_name = "{ENTER_BLOB_NAME}"
    meetings_table = '{ENTER_TABLE_NAME}'
    meetings_uri = "gs://zoom-data/list_of_meetings.jsonl"





    ssl._create_default_https_context = ssl._create_unverified_context
    today = dt.datetime.strftime(dt.datetime.utcnow(),'%Y-%m-%d')
    conn = http.client.HTTPSConnection("api.zoom.us")


    # Get jwt token for import
    token = generateToken()
    
    #List of all users
    get_all_users(token)
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    overwriteBigQueryTable(dataset,table,uri)

    #List of IM Groups
    get_all_imgroups(token)
    upload_blob(bucket_name, im_source_file_name, im_destination_blob_name)
    overwriteBigQueryTable(dataset,im_table,im_uri)

    #List of Meetings Groups
    get_meetings(token)
    upload_blob(bucket_name, meetings_source_file_name, meetings_destination_blob_name)
    appendBigQueryTable(dataset,meetings_table,meetings_uri)





    return f'Process complete.\n'





if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
