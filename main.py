import sqlite3
import json

from dotenv import load_dotenv
from gcal import get_events
from mlh_site import get_event_data
from db import get_probable_video
import csv

load_dotenv()
conn = sqlite3.connect('videos.db')

mlh_sites = []
mlh_site_data = []
with open('apiWeekEvents.json') as f:
    mlh_sites = json.load(f)
    for site in mlh_sites['sites']:
        try:
            event_data = get_event_data(site)
            twitch_url = get_probable_video(event_data['starts'])['url']
            del event_data['raw_data']
            event_data['twitch_url'] = twitch_url
            mlh_site_data.append(event_data)
        except Exception as e:
            print(f"Error when processing {site}", e)
            raise



csvFile = open('apiWeekEvents.csv', 'w')
csvWriter = csv.DictWriter(csvFile, fieldnames=mlh_site_data[0].keys())
csvWriter.writeheader()
csvWriter.writerows(mlh_site_data)
csvFile.close()
