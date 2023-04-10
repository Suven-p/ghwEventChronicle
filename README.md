## Setup

1. Create a .env file with `TWITCH_CLIENT_ID` and `TWITCH_CLIENT_SECRET` variables.
2. Install dependencies in requirements.txt preferably in a virtual environment.
3. Run twitch.py to get list of videos and create user_videos.json.
4. Run db.py to insert videos into a sqlite database.
5. Run main.py to create csv file.

## Structure
├── apiWeekEvents.csv           Final output
├── apiWeekEvents.json          JSON file of event url extracted manually
├── chromedriver_linux64        Attempt 1 to manually extract event url using selenium; not used
├── db.py                       Script to insert videos into sqlite database
├── main.py                     Script to create csv file
├── mlh_site.py                 Web scraping to get event title, start and end date and time
├── README.md                   This file
├── twitch.py                   Script to get list of videos and create user_videos.json
├── user_videos.json            JSON file of last 200 videos from MLH
└── videos.db                   Sqlite database of videos
